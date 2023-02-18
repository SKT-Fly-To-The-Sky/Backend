from pydantic import BaseModel


class User(BaseModel):
    userid: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FoodItemRequest(BaseModel):
    userid: str
    time_div: str

