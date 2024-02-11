from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.utils.log.logger import initialize_logging
from src.routers import game_params_router
from src.routers import leaderboard_router
from src.routers import score_router
from src.routers import user_router
from src.routers import word_router
from src.utils.init_db import init_db


app = FastAPI()


@app.on_event('startup')
def initialize_database():
    init_db()


# TODO add response validations on every route

app.include_router(user_router)
app.include_router(leaderboard_router)
app.include_router(score_router)
app.include_router(game_params_router)
app.include_router(word_router)


@app.exception_handler(HTTPException)
def my_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'code': exc.status_code,
            'message': exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
def my_validation_error_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    # Replace 'msg' with 'message' for each error
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


# Test route
@app.get('/healthy')
def index():
    return {
        "status": "healthy"
    }
