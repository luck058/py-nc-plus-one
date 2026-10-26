from fastapi import APIRouter
import logging
from typing import Any

from db.connection import get_from_db

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/rsvps")
def get_events(attendee_id: int|None = None, event_id: int|None = None) -> list[dict[str, Any]]:
    if attendee_id is None and event_id is None:
        return get_from_db("SELECT attendee_id, event_id FROM rsvps")
    elif attendee_id is None and event_id is not None:
        return get_from_db("SELECT attendee_id FROM rsvps WHERE event_id = %s", (event_id,))
    elif attendee_id is not None and event_id is None:
        return get_from_db("SELECT event_id FROM rsvps WHERE attendee_id = %s", (attendee_id,))
    else:
        raise ValueError("We shouldn't be able to get here")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )    

    logging.debug(get_events())
    logging.debug(get_events(attendee_id=1))
    logging.debug(get_events(event_id=1))
