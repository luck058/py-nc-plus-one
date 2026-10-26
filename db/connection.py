import psycopg2, os, logging
from dotenv import load_dotenv
from typing import Callable, Concatenate, ParamSpec, TypeVar, Any
from psycopg2.extensions import cursor
from functools import wraps

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")

load_dotenv()

def manage_cursor(func: Callable[Concatenate[cursor, P], R],
                  dbname: str|None = None,
                  user: str|None = None,
                  password: str|None = None) -> Callable[P, R]:
    #region Set db access info
    if not dbname:
        dbname = os.getenv("DB_NAME")
    if not user:
        user = os.getenv("DB_USER")
    if not password:
        password = os.getenv("DB_PASSWORD")
    else:
        logger.warning("It is recommended that you set you password in .env instead of passing it in")
    assert None not in [password, dbname, user], "Please fill out .env or pass in db access info"
    #endregion

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

@manage_cursor
def get_from_db(cur: cursor, query: str, vars: tuple|None = None) -> list[dict[str, Any]]:
    cur.execute(query, vars)
    assert cur.description is not None, f"The query: {query} with vars: {vars} did not generate a description"
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return [dict(zip(columns, row)) for row in rows]