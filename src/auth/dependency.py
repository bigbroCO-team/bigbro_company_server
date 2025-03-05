from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.factory.auth import AuthServiceFactory
from db import get_session


async def get_auth_service(session: AsyncSession = Depends(get_session)):
    return AuthServiceFactory.create(session)
