from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.LocationModel import Location
from repositories.LocationRepository import (
    LocationRepository,
)
from schemas.pydantic.LocationSchema import LocationSchema


class LocationService:
    locationsRepo: LocationRepository

    def __init__(
        self, locationsRepo: LocationRepository = Depends()
    ):
        self.locationsRepo = locationsRepo

    def create_location(
        self, location_data: LocationSchema
    ):
        location = Location(
            name=location_data.name,
            city=location_data.city,
        )

        return self.locationsRepo.create(location)

    def update_location(
        self,
        location_id: int,
        location_data: LocationSchema,
    ):
        location = Location(
            id=location_id,
            name=location_data.name,
            city=location_data.city,
        )

        return self.locationsRepo.update(location)

    def delete_location(self, location_id: int):
        location = self.locationsRepo.get_by_id(location_id)
        self.locationsRepo.delete(location)

    def get_location_by_id(self, location_id: int):
        return self.locationsRepo.get_by_id(location_id)

    def get_by_name(self, name: str):
        return self.locationsRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Location]:
        return self.locationsRepo.list(
            name, pageSize, startIndex
        )
