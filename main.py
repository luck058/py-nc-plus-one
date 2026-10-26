from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from routes.events import router as events_router
# from routes.rsvps import router as rsvps_router
# from routes.users import router as users_router
# from routes.venues import router as venues_router

app = FastAPI(title="NC Plus One API ", debug=True)
app.include_router(events_router)
# app.include_router(rsvps_router)
# app.include_router(users_router)
# app.include_router(venues_router)

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
