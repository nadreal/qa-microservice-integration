from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True  # allows returning SQLAlchemy models directly