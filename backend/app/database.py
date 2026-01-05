import os
import psycopg
from psycopg_pool import ConnectionPool
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10)

def get_db():
    with pool.connection() as conn:
        yield conn

@contextmanager
def get_db_context():
    with pool.connection() as conn:
        yield conn