from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class JobApplication(BaseModel):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = relationship(
        "JobApplicationStatus", back_populates="jobs_status"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "job_id": self.job_id.__str__(),
            "user_id": self.user_id.__str__(),
            "status": self.status.__str__(),
        }
