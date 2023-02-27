from typing import Optional, Dict, Any

from pydantic import BaseModel, root_validator, Field


class User(BaseModel):
    userid: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


#
# class IntakeRequest(BaseModel):
#     userid: str
#     time_div: str

class IntakeNutrientRequest(BaseModel):
    protein: float
    fat: float
    carbo: float
    sugar: float
    chole: float
    fiber: float
    calcium: float
    iron: float
    magne: float
    potass: float
    sodium: float
    zinc: float
    copper: float
    vitA: float
    vitB1: float
    vitB2: float
    vitB3: float
    vitB5: float
    vitB6: float
    vitB7: float
    vitB9: float
    vitB12: float
    vitC: float
    vitD: float
    vitE: float
    vitK: float
    omega: float
    kcal: float

    @classmethod
    def to_dict(cls, model_instance: 'IntakeNutrientRequest') -> Dict[str, Any]:
        return model_instance.dict()
