"""
Create the blob database and the table 
"""
import os
import sys
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "2287")
DB_NAME = os.getenv("DB_NAME", "blob_store")

async def create_db():
    """
    creates the database for the server
    """
    try:
        conn = await asyncpg.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        database_exists = await conn.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"
        )
        if not database_exists:
            await conn.execute(f"CREATE DATABASE {DB_NAME}")
            print("DB created!")
        else:
            print("DB exists!")
    except asyncpg.PostgresError as e:
        print(f"Error while creating database: {e}")
        sys.exit(1)
    finally:
        if conn:
            await conn.close()

    # connect to the correct db
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        await conn.execute(
            """
            DROP TABLE IF EXISTS files;
        """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                uuid UUID DEFAULT uuid_generate_v4(), 
                filename TEXT NOT NULL,
                file_type VARCHAR(255),
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        print("Table 'files' created (or already exists).")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        print("Table 'users' created (or already exists).")
    except asyncpg.PostgresError as e:
        print(f"Error while creating database: {e}")
        sys.exit(1)
    finally:
        if conn:
            await conn.close()


asyncio.run(create_db())
