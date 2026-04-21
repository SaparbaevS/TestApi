from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from api.api_v1.fastapi_users import current_active_user, current_active_super_user
from core.config import settings
from core.models import User
from core.schemas.user import UserRead

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)

@router.get("")
def get_user_message(
    user: Annotated[User, Depends(current_active_user)],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }

@router.get("/secrets")
def get_superuser_message(
    user: Annotated[User, Depends(current_active_super_user)],
):
    return {
        "messages": ["secrets-m1", "secrets-m2", "secrets-m3"],
        "user": UserRead.model_validate(user),
    }