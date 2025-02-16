from models.BaseModel import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class Job(BaseModel):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(4096), nullable=False)
    salary = Column(Numeric(10), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="jobs")
    new = Column(Boolean, nullable=False, default=False)
    remote = Column(Boolean, nullable=False, default=False)
    fullTime = Column(
        Boolean, nullable=False, default=False
    )
    partTime = Column(
        Boolean, nullable=False, default=False
    )
    featured = Column(
        Boolean, nullable=False, default=False
    )
    skills_id = Column(Integer, ForeignKey("skills.id"))
    skills = relationship(
        "Skills", lazy=True, back_populates="jobs"
    )
    active = Column(Boolean, nullable=False)
    categories = Column(Integer, nullable=False)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "title": self.title.__str__(),
            "description": self.description.__str__(),
            "salary": self.salary.__str__(),
            "company": self.company.__str__(),
            "new": self.new.__str__(),
            "remote": self.remote.__str__(),
            "fullTime": self.fullTime.__str__(),
            "partTime": self.partTime.__str__(),
            "featured": self.featured.__str__(),
            "skills": self.skills.__str__(),  # type: ignore
            "active": self.active.__str__(),
            "categories": self.categories.__str__(),  # type: ignore
        }
