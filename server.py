import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from db import create_db
from src.auth.presentation.controller.auth import router as auth_router
from config import SESSION_SECRET_KEY

app = FastAPI()


@app.get('/health-check')
async def root():
    return 'GOGO Minigame Service OK'


app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
app.include_router(auth_router)


if __name__ == '__main__':
    try:
        asyncio.run(create_db())
        uvicorn.run(app, host='0.0.0.0', port=8000)
    except Exception as e:
        print(e)
        exit(1)