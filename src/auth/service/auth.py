from abc import ABC, abstractmethod


class AuthService(ABC):
    @abstractmethod
    async def kakao_auth(self): pass

    @abstractmethod
    async def kakao_auth_callback(self, code, reqeust): pass