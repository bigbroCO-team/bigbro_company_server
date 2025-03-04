import asyncio

import uvicorn
from fastapi import FastAPI

from db import create_db

app = FastAPI()


@app.get('/health-check')
async def root():
    return 'GOGO Minigame Service OK'


if __name__ == '__main__':
    try:
        asyncio.run(create_db())
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        print(e)
        exit(1)