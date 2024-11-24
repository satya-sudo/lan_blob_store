import jwt
import os
import bcrypt
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from quart import Quart, request, jsonify, send_from_directory, Response

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "some_secret")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "12"))

def token_required(f):
    """
        decorator to check the auth token 
    """
    @wraps(f)
    async def check_token(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Un authorized!"}), 401
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token Invalid"}), 401
        return await f(*args, **kwargs)
    return check_token


app = {}

@app.route("register", methods=["POST"])
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
    hashed_password  = bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())
    async with app.db_pool.acquire() as conn:
        user_exists =  await conn.fetchval("SELECT COUNT(*) FROM users WHERE username = $1", username)
        if user_exists:
            return jsonify({"error": "username already exists."}), 400
        
        await conn.execute(
            "INSERT INTO users (username, password_hash) VALUES ($1, $2)",
            username,
            hashed_password.decode("utf-8")
        )
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
async def login():
    """
        Handler for login 
    """
    data = await request.json
    username =  data.get("username")
    password =  data.get("password")

    if not username and not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    async with app.db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT password_hash FROM users WHERE username = $1",username)
        if not row:
            return jsonify({"error": "username does not exists"}), 400
        stored_password_hash = row["password_hash"].encode("utf-8")
        if not bcrypt.checkpw(password=password,hashed_password=stored_password_hash):
            return jsonify({"error": "Invalid username or password"}), 401
        
        expiry = datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
        token =  jwt.encode({"username": username, "exp": expiry}, JWT_SECRET, algorithm="HS256")

    return jsonify({"token": token}), 200

@app.route("/reset", method=["POST"])
@token_required
async def reset():
    """
        handler to reset password
    """
    data = await request.json
    username = request.user['username']
    password =  data.get("old_password")
    new_pasword =  data.get("new_password")
    if not username and not password and not new_pasword:
        return jsonify({"error": "Username, password and new_password are required"}), 400
    async with app.db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT password_hash FROM users WHERE username = $1",username)
        if not row:
            return jsonify({"error": "username does not exists"}), 400
        stored_password_hash = row["password_hash"].encode("utf-8")
        if not bcrypt.checkpw(password=password,hashed_password=stored_password_hash):
            return jsonify({"error": "Invalid password"}), 401
        hashed_password  = bcrypt.hashpw(password=new_pasword.encode("utf-8"), salt=bcrypt.gensalt())
        
        await conn.execute(
            "UPDATE users SET password_hash = $1 WHERE username = $2",
            hashed_password.decode("utf-8"),
            username
        )
    return jsonify({"success": "password updated"}), 201
