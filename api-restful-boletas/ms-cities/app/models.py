from pydantic import BaseModel
from typing import Optional

class CityCreate(BaseModel):
    name: str
    country: str = "Colombia"
    timezone: str = "America/Bogota"
    is_active: bool = True

class CityResponse(BaseModel):
    id: int
    name: str
    country: str
    timezone: str
    is_active: bool

    class Config:
        from_attributes = True