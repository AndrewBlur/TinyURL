from .models import URL
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import text

def base62_encode(num:int):
    chars = "0123456789abcdefghijklmnopqrstuvwzxyABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return chars[0]

    result = ""
    while num > 0:
        num,rem = divmod(num,62)
        result = chars[rem]+result

    return result
        

async def check_db_connection(db: AsyncSession) -> bool:
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

async def insert_url(db:AsyncSession,original_url:str):
    try:
        url = URL(original_url=original_url)
        db.add(url)
        await db.flush()
        short_code = base62_encode(url.id)
        url.short_code = short_code
        await db.commit()
        return url.short_code
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500,detail="Error In DB call")


async def get_url(db:AsyncSession,short_code:str):
    try:
        stmt = select(URL).where(URL.short_code==short_code)
        result = await db.execute(stmt)
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=404,detail="No Record found")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500,detail=f"Error In DB call :{e}")
    
