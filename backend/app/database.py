import os
import psycopg
from psycopg_pool import ConnectionPool
from contextlib import contextmanager

# Use the environment variable from your Docker setup
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize a connection pool
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10)

def get_db():
    """
    FastAPI Dependency: yields a connection from the pool.
    The 'with' block ensures the connection is returned to the pool 
    even if an error occurs.
    """
    with pool.connection() as conn:
        yield conn

@contextmanager
def get_db_context():
    """
    A context manager version for use in non-FastAPI scripts 
    (like background tasks or standalone scripts).
    """
    with pool.connection() as conn:
        yield conn