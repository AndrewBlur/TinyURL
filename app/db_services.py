from .db import SessionLocal
from .models import URL
from sqlalchemy import select

db = SessionLocal()

def base62_encode(num:int):
    chars = "0123456789abcdefghijklmnopqrstuvwzxyABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return chars[0]

    result = ""
    while num > 0:
        num,rem = divmod(num,62)
        result = chars[rem]+result

    return result
        


def insert_url(original_url:str):
    url = URL(original_url=original_url)
    db.add(url)
    db.flush()
    short_code = base62_encode(url.id)
    url.short_code = short_code
    db.commit()


def get_url(short_code:str):
    stmt = select(URL).where(URL.short_code==short_code)
    result = db.execute(stmt).scalar_one_or_none()
    return result

