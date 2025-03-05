import httpx
from fastapi import HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service.auth import AuthService

from config import KAKAO_API_KEY, KAKAO_REDIRECT_URI, KAKAO_CLIENT_SECRET
from src.user.domain.model.user import User
from src.user.domain.repository.user import UserRepository


class AuthServiceImpl(AuthService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)

    async def kakao_auth(self):
        location =(
                f'https://kauth.kakao.com/oauth/authorize'
                f'?response_type=code'
                f'&client_id={KAKAO_API_KEY}'
                f'&redirect_uri={KAKAO_REDIRECT_URI}'
        )
        return RedirectResponse(url=location)

    async def kakao_auth_callback(self, code, request: Request):
        async with self.session.begin():
            access_token_res = await httpx.AsyncClient().post(
                url='https://kauth.kakao.com/oauth/token',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={
                    'grant_type': 'authorization_code',
                    'client_id': KAKAO_API_KEY,
                    'redirect_uri': KAKAO_REDIRECT_URI,
                    'code': code,
                    'client_secret': KAKAO_CLIENT_SECRET
                }
            )

            if not (access_token := access_token_res.json().get('access_token')):
                raise HTTPException(status_code=400, detail="Fail to signup")

            user_info_res = await httpx.AsyncClient().get(
                url="https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if not (user_email := user_info_res.json().get('kakao_account').get('email')):
                raise HTTPException(status_code=400, detail="Fail to signup")

            if not await self.user_repository.find_by_email(user_email):
                await self.user_repository.save(
                    User(
                        email=user_email
                    )
                )

            request.session['email'] = user_email

            return RedirectResponse(status_code=status.HTTP_302_FOUND, url='/')