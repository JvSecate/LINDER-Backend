from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Company(BaseModel):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    website = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location", lazy=True, back_populates="company")
    # location = Location()
    active = Column(Boolean, nullable=False)
    jobs = relationship("Job", back_populates="company")

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "website": self.website.__str__(),
            "email": self.email.__str__(),
            "description": self.description.__str__(),
            "location": self.location.__str__(),
            "active": self.active.__str__(),
        }