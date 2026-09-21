from fastapi import FastAPI,HTTPException,Depends
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from .init_db import init_db
from .schema import ShortenURLRequest
from sqlalchemy.ext.asyncio import AsyncSession
from .db_services import insert_url,get_url
from .db import get_db
from .cache import get_cached_url, cache_url
from dotenv import load_dotenv
load_dotenv()
import asyncio

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("APPLICATION STARTED")
    await init_db()

    yield

    print("APPLICATION SHUTTING DOWN")


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/shorten")
async def shorten_url(payload: ShortenURLRequest,db:AsyncSession = Depends(get_db)):
    short_code = await insert_url(db,str(payload.url))
    await cache_url(short_code,str(payload.url))
    return f"http://{os.environ.get("HOST")}:{os.environ.get("PORT")}/{short_code}"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/slow")
async def slow():
    await asyncio.sleep(10)
    return {"status": "done"}

@app.get("/{short_code}")
async def redirect_url(short_code:str,db:AsyncSession = Depends(get_db)):

    original_url = await get_cached_url(short_code)

    if original_url is None:

        url = await get_url(db,short_code)
        original_url = url.original_url

        await cache_url(short_code,original_url)

    return RedirectResponse(url=original_url)


