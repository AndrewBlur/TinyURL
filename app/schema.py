from pydantic import BaseModel, HttpUrl


class ShortenURLRequest(BaseModel):
    url:HttpUrl