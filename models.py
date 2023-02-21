from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Float, Text
from database import Base
from sqlalchemy.orm import relationship


# class FoodItemTable(Base):
#     __tablename__ = "food_items"
#
#     img_name = Column(String(300), primary_key=True)
#     userid = Column(String(50), ForeignKey('users.userid'))
#     date = Column(String(50))
#     time_div = Column(String(50))
#     image = Column(LargeBinary)
#
#     user = relationship("UserTable", backref="food_items")
#
#     def to_dict(self):
#         return {"id": self.id, "userid": self.userid, "name": self.name, "date": self.date}


class UserTable(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    userid = Column(String(50), primary_key=True)
    hashed_password = Column(String(100))
    physique = Column(String(100))
    nutrsuppl = Column(String(100))
    RDI = Column(String(100))

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)


class ConfigTable(Base):
    __tablename__ = "config_info"

    name = Column(String(50), primary_key=True, index=True)
    data = Column(Text)


class SupplementTable(Base):
    __tablename__ = "supplement_info"

    sup_name = Column(String(200), primary_key=True)
    intake_time_div = Column(String(50))
    buy_link = Column(String(300))
    sup_img = Column(LargeBinary(length=(2**24)-1))
    vitA = Column(Float)
    vitB1 = Column(Float)
    vitB2 = Column(Float)
    vitB3 = Column(Float)
    vitB5 = Column(Float)
    vitB6 = Column(Float)
    vitB7 = Column(Float)
    vitB9 = Column(Float)
    vitB12 = Column(Float)
    vitC = Column(Float)
    vitD = Column(Float)
    vitE = Column(Float)
    vitK = Column(Float)
    omega = Column(Float)
    kcal = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbo = Column(Float)
    sugar = Column(Float)
    chole = Column(Float)
    fiber = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    magne = Column(Float)
    potass = Column(Float)
    sodium = Column(Float)
    zinc = Column(Float)
    copper = Column(Float)


class FoodNutrientTable(Base):
    __tablename__ = "food_info"

    food_name = Column(String(100), primary_key=True)
    serving_size = Column(Float)
    kcal = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbo = Column(Float)
    sugar = Column(Float)
    chole = Column(Float)
    fiber = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    magne = Column(Float)
    potass = Column(Float)
    sodium = Column(Float)
    zinc = Column(Float)
    copper = Column(Float)
    vitA = Column(Float)
    vitB1 = Column(Float)
    vitB2 = Column(Float)
    vitB3 = Column(Float)
    vitB5 = Column(Float)
    vitB6 = Column(Float)
    vitB7 = Column(Float)
    vitB9 = Column(Float)
    vitB12 = Column(Float)
    vitC = Column(Float)
    vitD = Column(Float)
    vitE = Column(Float)
    vitK = Column(Float)
    omega = Column(Float)

    # def serialize(self):
    #     return {
    #         'food_name': self.food_name,
    #         'serving_size': self.serving_size,
    #         'kcal': self.kcal,
    #         'protein': self.protein,
    #         'fat': self.fat,
    #         'carbo': self.carbo,
    #         'sugar': self.sugar,
    #         'chole': self.chole,
    #         'fiber': self.fiber,
    #         'calcium': self.calcium,
    #         'iron': self.iron,
    #         'magne': self.magne,
    #         'potass': self.potass,
    #         'sodium': self.sodium,
    #         'zinc': self.zinc,
    #         'copper': self.copper,
    #         'vitA': self.vitA,
    #         'vitB1': self.vitB1,
    #         'vitB2': self.vitB2,
    #         'vitB3': self.vitB3,
    #         'vitB5': self.vitB5,
    #         'vitB6': self.vitB6,
    #         'vitB7': self.vitB7,
    #         'vitB9': self.vitB9,
    #         'vitB12': self.vitB12,
    #         'vitC': self.vitC,
    #         'vitD': self.vitD,
    #         'vitE': self.vitE,
    #         'vitK': self.vitK,
    #         'omega': self.omega,
    #     }


class RecommendedNutrientTable(Base):
    __tablename__ = "recommended_nut"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(String(10))
    gender = Column(String(10))
    vitA = Column(Float)
    vitB1 = Column(Float)
    vitB2 = Column(Float)
    vitB3 = Column(Float)
    vitB5 = Column(Float)
    vitB6 = Column(Float)
    vitB7 = Column(Float)
    vitB9 = Column(Float)
    vitB12 = Column(Float)
    vitC = Column(Float)
    vitD = Column(Float)
    vitE = Column(Float)
    vitK = Column(Float)
    omega = Column(Float)
    kcal = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbo = Column(Float)
    sugar = Column(Float)
    chole = Column(Float)
    fiber = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    magne = Column(Float)
    potass = Column(Float)
    sodium = Column(Float)
    zinc = Column(Float)
    copper = Column(Float)


class IntakeNutrientTable(Base):
    __tablename__ = "intake_nut"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(50), ForeignKey('users.userid'))
    date = Column(String(50))
    time = Column(DateTime)
    time_div = Column(String(10))
    image = Column(LargeBinary(length=(2**24)-1))
    kcal = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbo = Column(Float)
    sugar = Column(Float)
    chole = Column(Float)
    fiber = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    magne = Column(Float)
    potass = Column(Float)
    sodium = Column(Float)
    zinc = Column(Float)
    copper = Column(Float)
    vitA = Column(Float)
    vitB1 = Column(Float)
    vitB2 = Column(Float)
    vitB3 = Column(Float)
    vitB5 = Column(Float)
    vitB6 = Column(Float)
    vitB7 = Column(Float)
    vitB9 = Column(Float)
    vitB12 = Column(Float)
    vitC = Column(Float)
    vitD = Column(Float)
    vitE = Column(Float)
    vitK = Column(Float)
    omega = Column(Float)

    user = relationship("UserTable", backref="intakes")


'''
db 초기 세팅: alembic init migrations
revision 파일 생성: alembic revision --autogenerate \
revision db에 적용: alembic upgrade head
'''
