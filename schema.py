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
    time_div: str
    date: Optional[str]
    time: Optional[str]
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

    # @root_validator
    # def str_to_float(cls, values):
    #     except_col = ['time', 'time_div', 'date']
    #
    #     for k, v in values.items():
    #         if k in except_col:
    #             continue
    #         values[k] = float(v)
    #
    #     return values

    # class Config:
    #     # arbitrary_types_allowed = True
    #
    #     schema_extra = {
    #         'example': {
    #             'time_div': 'str',
    #             'date': '%Y-%m-%d',
    #             'time': 'str',
    #             'protein': 'str',
    #             'fat': 'str',
    #             'carbo': 'str',
    #             'sugar': 'str',
    #             'chole': 'str',
    #             'fiber': 'str',
    #             'calcium': 'str',
    #             'iron': 'str',
    #             'magne': 'str',
    #             'potass': 'str',
    #             'sodium': 'str',
    #             'zinc': 'str',
    #             'copper': 'str',
    #             'vitA': 'str',
    #             'vitB1': 'str',
    #             'vitB2': 'str',
    #             'vitB3': 'str',
    #             'vitB5': 'str',
    #             'vitB6': 'str',
    #             'vitB7': 'str',
    #             'vitB9': 'str',
    #             'vitB12': 'str',
    #             'vitC': 'str',
    #             'vitD': 'str',
    #             'vitE': 'str',
    #             'vitK': 'str',
    #             'omega': 'str',
    #             'kcal': 'str'
    #         }
    #     }

    @classmethod
    def to_dict(cls, model_instance: 'IntakeNutrientRequest') -> Dict[str, Any]:
        return model_instance.dict()



'''
    time_div: str
    date: Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    protein = Optional[str]
    fat = Optional[str]
    carbo = Optional[str]
    sugar = Optional[str]
    chole = Optional[str]
    fiber = Optional[str]
    calcium = Optional[str]
    iron = Optional[str]
    magne = Optional[str]
    potass = Optional[str]
    sodium = Optional[str]
    zinc = Optional[str]
    copper = Optional[str]
    vitA = Optional[str]
    vitB1 = Optional[str]
    vitB2 = Optional[str]
    vitB3 = Optional[str]
    vitB5 = Optional[str]
    vitB6 = Optional[str]
    vitB7 = Optional[str]
    vitB9 = Optional[str]
    vitB12 = Optional[str]
    vitC = Optional[str]
    vitD = Optional[str]
    vitE = Optional[str]
    vitK = Optional[str]
    omega = Optional[str]
    kcal = Optional[str]
'''

'''
class IntakeNutrientRequest(BaseModel):
    time_div: str
    date: Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    protein = Optional[str] = Field(
        ...,
        title='protein',
        description='This field is a float',
        example="float"
    )
    fat = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    carbo = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    sugar = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    chole = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    fiber = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    calcium = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    iron = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    magne = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    potass = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    sodium = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    zinc = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    copper = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitA = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB1 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB2 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB3 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB5 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB6 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB7 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB9 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitB12 = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitC = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitD = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitE = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    vitK = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    omega = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
    kcal = Optional[str] = Field(
        ...,
        title='nut_info',
        description='This field is a float',
        example="float"
    )
'''
'''
time_div: str
    date: Optional[str]
    time: Optional[str]
    protein = str
    fat = str
    carbo = str
    sugar = str
    chole = str
    fiber = str
    calcium = str
    iron = str
    magne = str
    potass = str
    sodium = str
    zinc = str
    copper = str
    vitA = str
    vitB1 = str
    vitB2 = str
    vitB3 = str
    vitB5 = str
    vitB6 = str
    vitB7 = str
    vitB9 = str
    vitB12 = str
    vitC = str
    vitD = str
    vitE = str
    vitK = str
    omega = str
    kcal = str
'''
'''
{
  "time_div": "점심",
  "date": "2023-02-19",
  "time": "2023-02-19 12:05:32",
  "protein": "1",
  "fat": "1",
  "carbo": "1",
  "sugar": "1",
  "chole": "1",
  "fiber": "1",
  "calcium": "1",
  "iron": "1",
  "magne": "1",
  "potass": "1",
  "sodium": "1",
  "zinc": "1",
  "copper": "1",
  "vitA": "1",
  "vitB1": "1",
  "vitB2": "1",
  "vitB3": "1",
  "vitB5": "1",
  "vitB6": "1",
  "vitB7": "1",
  "vitB9": "1",
  "vitB12": "1",
  "vitC": "1",
  "vitD": "1",
  "vitE": "1",
  "vitK": "1",
  "omega": "1",
  "kcal": "1"
}
'''

'''
{
  "time_div": "점심",
  "date": "2023-02-19",
  "time": "2023-02-19 12:05:32",
  "protein": 1,
  "fat": 1,
  "carbo": 1,
  "sugar": 1,
  "chole": 1,
  "fiber": 1,
  "calcium": 1,
  "iron": 1,
  "magne": 1,
  "potass": 1,
  "sodium": 1,
  "zinc": 1,
  "copper": 1,
  "vitA": 1,
  "vitB1": 1,
  "vitB2": 1,
  "vitB3": 1,
  "vitB5": 1,
  "vitB6": 1,
  "vitB7": 1,
  "vitB9": 1,
  "vitB12": 1,
  "vitC": 1,
  "vitD": 1,
  "vitE": 1,
  "vitK": 1,
  "omega": 1,
  "kcal": 1
}
'''