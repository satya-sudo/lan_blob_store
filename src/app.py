"""
    server the server in production
"""
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from server.config import create_app, SERVER_HOST, SERVER_PORT
from server.db import create_db_pool, close_db_pool
from auth.routes import auth_bp
from files.routes import files_bp

app = create_app()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(files_bp, url_prefix="/files")

# Database lifecycle
app.before_serving(create_db_pool)
app.after_serving(close_db_pool)

config = Config()
config.bind = [f"{SERVER_HOST}:{SERVER_PORT}"]

asyncio.run(serve(app, config))
