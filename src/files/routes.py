"""
    Routes and controller for file and blob, stream store
"""
import os
import shutil
import uuid
from datetime import datetime
import aiofiles
from quart import Blueprint, request, jsonify, \
    send_from_directory, Response, current_app
from auth.auth_middleware import token_required

files_bp = Blueprint("files", __name__)


@files_bp.route("/", methods=["GET"])
async def index():
    """
        Index and status api
    """

    total, used, free = shutil.disk_usage("/")

    # Convert bytes to GB for readability
    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)

    response_data = {
        "Status": "UP",
        "TotalSpace": f"{total_gb} GB",
        "FreeSpace": f"{used_gb} GB",
        "UsedSpace": f"{free_gb} GB",
    }

    return jsonify(response_data), 200


@files_bp.route("/upload", methods=["POST"])
@token_required
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
    file_type = file.content_type
    file_name = file.filename.replace(" ", "_")
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], file_uuid + "_" + file_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file.read())

    # Store file metadata in the database
    async with current_app.db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO files (uuid, filename, file_type, upload_time) VALUES ($1, $2, $3, $4)",
            file_uuid,
            file_name,
            file_type,
            datetime.now(),
        )

    return (
        jsonify(
            {"message": f"File {file_name} uploaded successfully", "uuid": file_uuid}
        ),
        201,
    )


@files_bp.route("/files", methods=["GET"])
@token_required
async def list_files():
    """
    Retrieve file metadata from the database
    """
    async with current_app.db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, uuid, filename, file_type, upload_time FROM files")
        files = [
            {
                "id": row["id"],
                "uuid": row["uuid"],
                "filename": row["filename"],
                "filetype": row["file_type"],
                "upload_time": row["upload_time"],
            }
            for row in rows
        ]

    return jsonify(files)


@files_bp.route("/download/<fileuuid>", methods=["GET"])
@token_required
async def download_file(fileuuid):
    """Serve file asynchronously by UUID for download."""

    async with current_app.db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT filename FROM files WHERE uuid = $1", fileuuid
        )

        if not row:
            return jsonify({"error": "File not found"}), 404
        # Construct file path
        filename = row["filename"]
        file_path = f"{fileuuid}_{filename}"
        return await send_from_directory(
            current_app.config["UPLOAD_FOLDER"], f"{file_path}", as_attachment=True
        )


@files_bp.route("/stream/<fileuuid>", methods=["GET"])
async def stream_video(fileuuid):
    """
    Stream video content with support for range requests
    """
    async with current_app.db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT filename, file_type FROM files WHERE uuid = $1", fileuuid)
        if not row:
            return jsonify({"error": "File not found"}), 404

        file_type = row["file_type"]
        if not file_type.startswith("video/"):
            return jsonify({"error": "Requested file is not a video"}), 400
        filename = row["filename"]
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], f"{fileuuid}_{filename}")

        range_header = request.headers.get('Range', None)
        file_size = os.path.getsize(file_path)

        if range_header:
            start, end = range_header.replace("bytes=", "").split("-")
            start = int(start)
            end = int(end) if end else file_size - 1
        else:
            start, end = 0, file_size - 1

        async with aiofiles.open(file_path, "rb") as f:
            await f.seek(start)
            chunk_size = end - start + 1
            data = await f.read(chunk_size)

        response = Response(data, status=206, mimetype=file_type)
        response.headers.add(
            "Content-Range", f"bytes {start}-{end}/{file_size}")
        response.headers.add("Accept-Ranges", "bytes")
        response.headers.add("Content-Length", str(chunk_size))

        return response
