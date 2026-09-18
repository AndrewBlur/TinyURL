from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import RedirectResponse
from .init_db import init_db
from .schema import ShortenURLRequest
from sqlalchemy.ext.asyncio import AsyncSession
from .db_services import insert_url,get_url
from .db import get_db
from dotenv import load_dotenv
load_dotenv()

import os

app = FastAPI()



@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/shorten")
async def shorten_url(payload: ShortenURLRequest,db:AsyncSession = Depends(get_db)):
    short_code = await insert_url(db,str(payload.url))
    return f"http://{os.environ.get("HOST")}:{os.environ.get("PORT")}/{short_code}"

@app.get("/{short_code}")
async def redirect_url(short_code:str,db:AsyncSession = Depends(get_db)):

    url = await get_url(db,short_code)
    return RedirectResponse(url=url.original_url,)
