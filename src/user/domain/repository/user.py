from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.user.domain.model.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User):
        self._session.add(user)

    async def find_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await self._session.exec(statement)
        return result.first()