from models.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class JobApplicationStatus(BaseModel):
    __tablename__ = "job_application_statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    jobs_application_id = Column(
        Integer, ForeignKey("job_applications.id")
    )
    jobs_status = relationship(
        "JobApplication", back_populates="status"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
