from http import HTTPStatus

from fastapi import APIRouter

from app.database.engine import check_availability
from app.models.app import AppStatus

router = APIRouter()


@router.get('/status', response_model=AppStatus, status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    return AppStatus(database=check_availability(), status='App run successful')
