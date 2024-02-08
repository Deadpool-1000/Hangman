from fastapi import APIRouter, Depends
from starlette import status

from src.controllers import ScoreController
from src.schemas import ScoreSchema
from src.utils.jwt_helper import get_token

score_router = APIRouter(tags=['Score'])


@score_router.put('/score', summary='Update score', status_code=status.HTTP_200_OK)
def update_score(score_data: ScoreSchema, token=Depends(get_token)):
    user_id = token['sub']
    success_message = ScoreController.update_score(user_id, score_data.model_dump())
    return success_message
