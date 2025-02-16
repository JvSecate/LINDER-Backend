from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String

class JobCategory(BaseModel):
    __tablename__ = "job_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }