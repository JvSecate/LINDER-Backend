from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.LocationModel import Location


class LocationRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, location: Location) -> Location:
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def update(self, location: Location) -> Location | None:
        self.db.merge(location)
        self.db.commit()

        return location

    def delete(self, location: Location) -> None:
        self.db.delete(location)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Location]:
        query = self.db.query(Location)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Location:
        return self.db.query(Location).get(id)

    def get_by_name(self, name: str) -> Location:
        return (
            self.db.query(Location)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[Location]:
        return self.db.query(Location).all()
