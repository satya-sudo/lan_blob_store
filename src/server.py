"""
Blob store 
"""
import os
import uuid
import asyncio
from datetime import datetime
from hypercorn.config import Config
from hypercorn.asyncio import serve
from quart import Quart, request, jsonify, send_from_directory
from dotenv import load_dotenv
import aiofiles
import asyncpg

load_dotenv()
app = Quart(__name__)

# server ports
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", "5872")

# Database connection settings
DB_NAME = os.getenv("DB_NAME", "blob_store")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BLOB_LOCATION = os.getenv("BLOB_LOCATION", "~/blob_store")
UPLOAD_FOLDER = os.path.expanduser(BLOB_LOCATION)


print(DB_PASSWORD)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.before_serving
async def create_db_pool():
    """
    connect to db
    """
    try:
        app.db_pool = await asyncpg.create_pool(DATABASE_URL)
    except (asyncpg.exceptions.ConnectionDoesNotExistError, 
            asyncpg.exceptions.InvalidCatalogNameError) as e:
        print(f"Database connection error: {e}")
        app.db_pool = None
    except Exception as e:
        print(f"An error occurred while creating the database pool: {e}")
        app.db_pool = None


@app.after_serving
async def close_db_pool():
    """
    close the db connection
    """
    await app.db_pool.close()


@app.route("/upload", methods=["POST"])
async def upload_file():
    """
    upload file to disk and update entry in the db
    """
    
    files = await request.files
    if "file" not in files:
        return jsonify({"error": "No file part in the request"}), 400
    file = files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save file asynchronously
    file_uuid = str(uuid.uuid4())
    file_name = file.filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_FOLDER, file_uuid + "_" + file_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file.read())

    # Store file metadata in the database
    async with app.db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO files (uuid, filename, upload_time) VALUES ($1, $2, $3)",
            file_uuid,
            file_name,
            datetime.now(),
        )

    return (
        jsonify(
            {"message": f"File {file_name} uploaded successfully", "uuid": file_uuid}
        ),
        201,
    )


@app.route("/files", methods=["GET"])
async def list_files():
    """
    Retrieve file metadata from the database
    """
    async with app.db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, uuid, filename, upload_time FROM files")
        files = [
            {
                "id": row["id"],
                "uuid": row["uuid"],
                "filename": row["filename"],
                "upload_time": row["upload_time"],
            }
            for row in rows
        ]

    return jsonify(files)


@app.route("/download/<fileuuid>", methods=["GET"])
async def download_file(fileuuid):
    """Serve file asynchronously by UUID for download."""

    async with app.db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT filename FROM files WHERE uuid = $1", fileuuid
        )
        print("Sdf", row)

        if not row:
            return jsonify({"error": "File not found"}), 404
        # Construct file path
        filename = row["filename"]
        file_path = f"{fileuuid}_{filename}"
        return await send_from_directory(
            UPLOAD_FOLDER, f"{file_path}", as_attachment=True
        )



# runing the server in production
config = Config()
config.bind = [f"{SERVER_HOST}:{SERVER_PORT}"]

asyncio.run(serve(app, config))
