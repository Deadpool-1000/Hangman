import src.config.helper
from fastapi import FastAPI

from dotenv import load_dotenv

from src.routers import user_router
from src.routers import leaderboard_router
from src.routers import game_params_router
from src.routers import score_router
from src.routers import word_router


load_dotenv()
app = FastAPI()

app.include_router(user_router)
app.include_router(leaderboard_router)
app.include_router(score_router)
app.include_router(game_params_router)
app.include_router(word_router)


# Test route
@app.get('/')
def index():
    return {
        "message": "Hello World!"
    }

