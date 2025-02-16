from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Country(BaseModel):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    initials = Column(String(50), nullable=False)

    states = relationship(
        "State", back_populates="country", 
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "initials": self.initials.__str__(),
            "states": self.states.__str__(),
        }
