from quart import Quart, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import aiofiles
from datetime import datetime
import asyncpg
import uuid

load_dotenv()
app = Quart(__name__)

# Database connection settings

DB_NAME = os.getenv("DB_NAME", "blob_store")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BLOB_LOCATION = os.getenv("BLOB_LOCATION", "~/blob_store")
UPLOAD_FOLDER = os.path.expanduser(BLOB_LOCATION)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.before_serving
async def create_db_pool():
    """
    connect to db
    """
    app.db_pool = await asyncpg.create_pool(DATABASE_URL)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5658)
