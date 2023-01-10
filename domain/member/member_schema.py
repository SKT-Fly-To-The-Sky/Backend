from pydantic import BaseModel


class Member(BaseModel):
    id: int
    account: str # | None = None

    class Config:
        orm_mode = True
