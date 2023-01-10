from datetime import datetime

from pydantic import BaseModel


class Picture(BaseModel):
    id: int
    member_id: int
    date: datetime
    image_name: str

    class Config:
        orm_mode = True
