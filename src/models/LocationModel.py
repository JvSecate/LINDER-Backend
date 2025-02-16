from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Location(BaseModel):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship(
        "City",
        lazy=True,
        back_populates="location",
    )
    company = relationship("Company", back_populates="location", lazy=True)
    address = Column(String(50), nullable=False)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "city": self.city.__str__(),
            "address": self.address.__str__(),
        }
