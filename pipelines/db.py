"""Shared Postgres connection. Auto-falls back to OS user when 'postgres' role doesn't exist (local Mac)."""
import os
import getpass
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()


def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "saas_platform")

    attempts = [
        (
            os.getenv("POSTGRES_USER") or "postgres",
            os.getenv("POSTGRES_PASSWORD") or "postgres",
        ),
        (getpass.getuser(), ""),
    ]

    last_error = None
    for user, password in attempts:
        url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        engine = create_engine(url)
        try:
            with engine.connect():
                pass
            return engine
        except OperationalError as e:
            last_error = e
            err_msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
            if "does not exist" in err_msg and user == (os.getenv("POSTGRES_USER") or "postgres"):
                continue
            raise
    raise last_error
