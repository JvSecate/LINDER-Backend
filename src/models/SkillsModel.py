from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Skills(BaseModel):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    jobs = relationship(
        "Job", lazy=True, back_populates="skills"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
