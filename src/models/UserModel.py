from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)
    profile = Column(String(50), nullable=False)
    experience = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "email": self.email.__str__(),
            "phone": self.phone.__str__(),
            "profile": self.profile.__str__(),
            "experience": self.experience.__str__(),
            "password": self.password.__str__(),
        }
