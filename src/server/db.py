"""
    handle db access pool
"""
import asyncpg
from quart import current_app

async def create_db_pool():
    """
    Create database connection pool
    """
    try:
        current_app.db_pool =  await asyncpg.create_pool(
            current_app.config["DATABASE_URL"]
        )
    except (asyncpg.exceptions.ConnectionDoesNotExistError, 
            asyncpg.exceptions.InvalidCatalogNameError) as e:
        print(f"Database connection error: {e}")
        current_app.db_pool = None
    except Exception as e: # handle other errors
        print(f"An error occurred while creating the database pool: {e}")
        current_app.db_pool = None

async def close_db_pool():
    """
    Close the database connection pool
    """
    if current_app.db_pool:
        await current_app.db_pool.close()
