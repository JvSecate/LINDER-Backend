from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.JobApplicationModel import (
    JobApplication,
)
''

class JobApplicationRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(
        self, jobApplicationStatus: JobApplication
    ) -> JobApplication:
        self.db.add(jobApplicationStatus)
        self.db.commit()
        self.db.refresh(jobApplicationStatus)
        return jobApplicationStatus

    def update(
        self, jobApplicationStatus: JobApplication
    ) -> JobApplication | None:
        self.db.merge(jobApplicationStatus)
        self.db.commit()

        return jobApplicationStatus

    def delete(
        self, jobApplicationStatus: JobApplication
    ) -> None:
        self.db.delete(jobApplicationStatus)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[JobApplication]:
        query = self.db.query(JobApplication)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> JobApplication:
        return self.db.query(JobApplication).get(id)

    def get_by_name(
        self, name: str
    ) -> JobApplication:
        return (
            self.db.query(JobApplication)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[JobApplication]:
        return self.db.query(JobApplication).all()
