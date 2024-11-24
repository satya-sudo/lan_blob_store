"""
    Set up the config for the server
    create app 
"""

import os
from dotenv import load_dotenv
from quart import Quart

load_dotenv()

# load config from .env
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "5872"))
DB_NAME = os.getenv("DB_NAME", "blob_store")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "2287")
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "12"))

# database and storage
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
UPLOAD_FOLDER = os.path.expanduser(os.getenv("BLOB_LOCATION", "~/blob_store"))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app():
    """
        create Quart server instance 
    """
    app = Quart(__name__)
    app.config["SERVER_HOST"] = SERVER_HOST
    app.config["SERVER_PORT"] = SERVER_PORT
    app.config["DB_NAME"] = DB_NAME
    app.config["DB_USER"] = DB_USER
    app.config["DB_PASSWORD"] = DB_PASSWORD
    app.config["DB_HOST"] = DB_HOST
    app.config["DB_PORT"] = DB_PORT
    app.config["JWT_SECRET"] = JWT_SECRET
    app.config["JWT_EXPIRY_HOURS"] = int(JWT_EXPIRY_HOURS)
    app.config["DATABASE_URL"] = DATABASE_URL
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    return app
