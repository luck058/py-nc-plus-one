import psycopg2, os, logging
from dotenv import load_dotenv
from typing import Callable, Concatenate, ParamSpec, TypeVar
from psycopg2.extensions import cursor
from functools import wraps

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")

load_dotenv()
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")

assert None not in [password, dbname, user], "Please fill out .env"

def manage_cursor(func: Callable[Concatenate[cursor, P], R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password
        )
        cur = conn.cursor()
        try:
            result = func(cur, *args, **kwargs)
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return result
    return wrapper