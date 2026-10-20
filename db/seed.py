import logging
from psycopg2.extensions import cursor
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

def insert_test_data(cur: cursor) -> None:
    logging.debug("Inserting Test Data")
    raise NotImplementedError

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