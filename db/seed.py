import logging, json
from psycopg2.extensions import cursor
from psycopg2 import sql
from psycopg2.extras import execute_values

from db.connection import manage_cursor

logger = logging.getLogger(__name__)


def remove_old_data(cur: cursor) -> None:
    logging.debug("Removing Old Data")
    cur.execute("""
    DROP TABLE IF EXISTS
        Rsvps,
        Events,
        Venues,
        Users
    CASCADE
    """)

def rebuild_table_schemas(cur: cursor) -> None:
    logging.debug("Rebuilding Schema")
    cur.execute("""
    CREATE TABLE Venues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address TEXT,
        capacity INT
    )
    """)

    cur.execute("""
    CREATE TABLE Users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """)

    cur.execute("""
    CREATE TABLE Events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255),
        starts_at TIMESTAMPTZ NOT NULL,
        ends_at TIMESTAMPTZ NOT NULL,
        organiser_id INT REFERENCES Users(id),
        venue_id INT REFERENCES Venues(id),
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """)

    cur.execute("""
    CREATE TABLE Rsvps (
        id SERIAL PRIMARY KEY,
        attendee_id INT REFERENCES Users(id),
        event_id INT REFERENCES Events(id),
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """)

def load_data(cur: cursor, json_file: str, table: str) -> None:
    assert json_file.split(".")[-1] == "json", "Please enter a json file"
    logging.debug(f"Inserting data from {json_file}")

    with open(json_file) as f:
        rows = json.load(f)

    if not rows:
        logging.warning(f"No data was loaded from {json_file}")
        return

    columns = list(rows[0].keys())
    values = [[row[col] for col in columns] for row in rows]

    query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table),
        sql.SQL(", ").join(map(sql.Identifier, columns)),
    )
    execute_values(cur, query, values)

def insert_test_data(cur: cursor) -> None:
    data_loc = "db/data/"
    load_data(cur, data_loc + "users.json", "users")
    load_data(cur, data_loc + "venues.json", "venues")
    load_data(cur, data_loc + "events.json", "events")
    load_data(cur, data_loc + "rsvps.json", "rsvps")

@manage_cursor
def seed(cur: cursor) -> None:
    logging.info("Seeding database")
    remove_old_data(cur)
    rebuild_table_schemas(cur)
    insert_test_data(cur)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    seed()