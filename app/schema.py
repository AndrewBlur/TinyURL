from pydantic import BaseModel


class ShortenURLRequest(BaseModel):
    url:str