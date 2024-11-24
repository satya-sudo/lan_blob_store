"""
    handle auth and jwt for routes

"""
from functools import wraps
import jwt
from quart import request, jsonify, current_app
from .utils import decode_jwt

def token_required(f):
    """
        wrapper for auth routes
    """
    @wraps(f)
    async def decorated(*args, **kwargs):
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing or invalid"}), 401

        token = auth_header.split(" ")[1]  # Get the token part

        try:
            # Decode the token using the app's JWT_SECRET
            decoded_token = decode_jwt(token, current_app.config["JWT_SECRET"])
            request.user = decoded_token  # Attach user data to the request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Proceed to the route handler
        return await f(*args, **kwargs)

    return decorated
