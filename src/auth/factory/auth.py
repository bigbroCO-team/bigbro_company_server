from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service.auth import AuthService
from src.auth.service.impl.auth import AuthServiceImpl
from db import get_session


def get_auth_service(session: Annotated[AsyncSession, Depends(get_session)]) -> AuthService:
    return AuthServiceImpl(session)