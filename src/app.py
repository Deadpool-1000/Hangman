from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from src.routers import game_params_router
from src.routers import leaderboard_router
from src.routers import score_router
from src.routers import user_router
from src.routers import word_router

app = FastAPI()

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


# Test route
@app.get('/healthy')
def index():
    return {
        "status": "healthy"
    }
