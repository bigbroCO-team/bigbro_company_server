from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.params import Param

from src.auth.dependency import get_auth_service
from src.auth.service.auth import AuthService

router = APIRouter(prefix='/auth')


@router.get('/kakao')
async def kakao_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.kakao_auth()


@router.get('/kakao/callback')
async def kakao_auth_callback(
        code: Annotated[str, Param],
        request: Request,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.kakao_auth_callback(code, request)