from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .CountryModel import Country

class State(BaseModel):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    initials = Column(String(50), nullable=False)
    country_id = Column(
        Integer, ForeignKey("countries.id"), nullable=False
    )

    cities = relationship(
        "City",
        back_populates="state",
    )
    country = relationship(Country, back_populates="states")

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "initials": self.initials.__str__(),
            "cities": self.cities.__str__(),
        }
