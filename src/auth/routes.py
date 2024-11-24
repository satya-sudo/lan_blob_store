"""
    routes and handlers
    for auth
"""

from quart import Blueprint, request, jsonify, current_app
from .utils import hash_password, verify_password, create_jwt
from .auth_middleware import token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("register", methods=["POST"])
async def register():
    """
        handler to register the user
    """
    data = await request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # hash the password
    hashed_password = hash_password(password=password)
    async with current_app.db_pool.acquire() as conn:
        user_exists = await conn.fetchval(
        "SELECT COUNT(*) FROM users WHERE username = $1",
        username
        )
        if user_exists:
            return jsonify({"error": "username already exists."}), 400

        await conn.execute(
            "INSERT INTO users (username, password_hash) VALUES ($1, $2)",
            username,
            hashed_password
        )
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
async def login():
    """
        Handler for login 
    """
    data = await request.json
    username = data.get("username")
    password = data.get("password")

    if not username and not password:
        return jsonify({"error": "Username and password are required"}), 400

    async with current_app.db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT password_hash FROM users WHERE username = $1", username)
        if not row or not verify_password(password=password, hashed=row["password_hash"]):
            return jsonify({"error": "username does not exists"}), 400

        token = create_jwt(
            username=username,
            secret=current_app.config["JWT_SECRET"],
            expiry_hours=current_app.config["JWT_EXPIRY_HOURS"])

    return jsonify({"token": token}), 200


@auth_bp.route("/reset", method=["POST"])
@token_required
async def reset():
    """
        handler to reset password
    """
    data = await request.json
    username = request.user['username']
    password = data.get("old_password")
    new_pasword = data.get("new_password")
    if not username and not password and not new_pasword:
        return jsonify({"error": "Username, password and new_password are required"}), 400
    async with current_app.db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT password_hash FROM users WHERE username = $1", username)
        if not row:
            return jsonify({"error": "username does not exists"}), 400
        stored_password_hash = row["password_hash"]
        if not verify_password(password=password, hashed=stored_password_hash):
            return jsonify({"error": "Invalid password"}), 401
        hashed_password = hash_password(password=new_pasword)

        await conn.execute(
            "UPDATE users SET password_hash = $1 WHERE username = $2",
            hashed_password.decode("utf-8"),
            username
        )
    return jsonify({"success": "password updated"}), 201
