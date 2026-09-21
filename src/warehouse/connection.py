import psycopg2
from sqlalchemy import create_engine
from contextlib import contextmanager
from src.utils.config import logger, get_db_url, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER

class DatabaseConnectionError(Exception):
    pass

@contextmanager
def get_postgres_connection():
    """Context manager for psycopg2 connections."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        yield conn
    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise DatabaseConnectionError(f"Connection failed: {e}")
    finally:
        if conn:
            conn.close()

def get_sqlalchemy_engine():
    """Returns a SQLAlchemy engine."""
    try:
        engine = create_engine(get_db_url())
        return engine
    except Exception as e:
        logger.error(f"Failed to create SQLAlchemy engine: {e}")
        raise DatabaseConnectionError(f"Engine creation failed: {e}")
