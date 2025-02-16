from sqlalchemy import Column, Integer, String, ForeignKey
from models.BaseModel import BaseModel
from sqlalchemy.orm import relationship

from models.StateModel import State

class City(BaseModel):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    state_id = Column(
        Integer, ForeignKey("states.id"), nullable=False
    )
    state = relationship(State, back_populates="cities")
    location = relationship(
        "Location",
        lazy=True,
        back_populates="city",
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "state": self.state.__str__(),
            "state_id": self.state_id.__str__(),
        }
