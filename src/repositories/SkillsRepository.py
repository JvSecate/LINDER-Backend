from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.SkillsModel import Skills


class SkillsRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, skills: Skills) -> Skills:
        self.db.add(skills)
        self.db.commit()
        self.db.refresh(skills)
        return skills

    def update(self, skills: Skills) -> Skills | None:
        self.db.merge(skills)
        self.db.commit()

        return skills

    def delete(self, skills: Skills) -> None:
        self.db.delete(skills)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Skills]:
        query = self.db.query(Skills)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Skills:
        return self.db.query(Skills).get(id)

    def get_by_name(self, name: str) -> Skills:
        return (
            self.db.query(Skills).filter_by(name=name).all()
        )

    def get_all(self) -> List[Skills]:
        return self.db.query(Skills).all()
