from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service.auth import AuthService
from src.auth.service.impl.auth import AuthServiceImpl


class AuthServiceFactory:
    @staticmethod
    def create(session: AsyncSession) -> AuthService:
        return AuthServiceImpl(session)
