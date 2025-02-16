from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.JobCategoryModel import JobCategory


class JobCategoryRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(
        self, jobCategory: JobCategory
    ) -> JobCategory:
        self.db.add(jobCategory)
        self.db.commit()
        self.db.refresh(jobCategory)
        return jobCategory

    def update(
        self, jobCategory: JobCategory
    ) -> JobCategory | None:
        self.db.merge(jobCategory)
        self.db.commit()

        return jobCategory

    def delete(self, jobCategory: JobCategory) -> None:
        self.db.delete(jobCategory)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[JobCategory]:
        query = self.db.query(JobCategory)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> JobCategory:
        return self.db.query(JobCategory).get(id)

    def get_by_name(self, name: str) -> JobCategory:
        return (
            self.db.query(JobCategory)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[JobCategory]:
        return self.db.query(JobCategory).all()
