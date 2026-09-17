from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .init_db import init_db
from .schema import ShortenURLRequest
from .db_services import insert_url,get_url
app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/shorten")
async def shorten_url(payload: ShortenURLRequest):
    insert_url(payload.url)

    return {"result":"success"}

@app.get("/{short_code}")
async def redirect_url(short_code:str):
    url = get_url(short_code)
    return RedirectResponse(url=url.original_url)