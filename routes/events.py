from fastapi import APIRouter
import logging
from typing import Any

from db.connection import get_from_db

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/events")
def get_events() -> list[dict[str, Any]]:
    # Only key info is sent. Further information can be requested by id
    return get_from_db("SELECT id, title, description FROM events")

@router.get("/events/{id}")
def get_event_by_id(id: int) -> dict[str, Any]:
    event_info = get_from_db("SELECT * FROM events WHERE id = %s", (id,))
    assert len(event_info) == 1
    return get_from_db("SELECT * FROM events WHERE id = %s", (id,))[0]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )    

    logging.debug(get_event_by_id(1))
