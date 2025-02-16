from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.JobApplicationStatusModel import (
    JobApplicationStatus,
)


class JobApplicationStatusRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(
        self, jobApplicationStatus: JobApplicationStatus
    ) -> JobApplicationStatus:
        self.db.add(jobApplicationStatus)
        self.db.commit()
        self.db.refresh(jobApplicationStatus)
        return jobApplicationStatus

    def update(
        self, jobApplicationStatus: JobApplicationStatus
    ) -> JobApplicationStatus | None:
        self.db.merge(jobApplicationStatus)
        self.db.commit()

        return jobApplicationStatus

    def delete(
        self, jobApplicationStatus: JobApplicationStatus
    ) -> None:
        self.db.delete(jobApplicationStatus)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[JobApplicationStatus]:
        query = self.db.query(JobApplicationStatus)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> JobApplicationStatus:
        return self.db.query(JobApplicationStatus).get(id)

    def get_by_name(
        self, name: str
    ) -> JobApplicationStatus:
        return (
            self.db.query(JobApplicationStatus)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[JobApplicationStatus]:
        return self.db.query(JobApplicationStatus).all()
