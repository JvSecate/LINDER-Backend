from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Numeric


class Comment(BaseModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment = Column(String(200), nullable=False)
    job_id = Column(Integer, nullable=False)
    likes = Column(Numeric(5), nullable=False)
    unlikes = Column(Numeric(5), nullable=False)


    def normalize(self):
        return {
            "id": self.id.__str__(),
            "comment": self.comment.__str__(),
            "job_id": self.job_id.__str__(),
            "likes": self.likes.__str__(),
            "unlikes": self.unlikes.__str__(),
        }