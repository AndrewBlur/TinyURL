from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from .db import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, nullable=True, index=True)
    original_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
