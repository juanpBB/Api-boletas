from pydantic import BaseModel
from typing import Optional

class PointOfSaleCreate(BaseModel):
    name: str
    address: str
    city_id: int
    phone: Optional[str] = None
    is_active: bool = True

class PointOfSaleResponse(BaseModel):
    id: int
    name: str
    address: str
    city_id: int
    phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True