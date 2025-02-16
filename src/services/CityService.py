from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.CityModel import City
from repositories.CityRepository import CityRepository
from schemas.pydantic.CitySchema import CitySchema


class CityService:
    citiesRepo: CityRepository

    def __init__(
        self, citiesRepo: CityRepository = Depends()
    ):
        self.citiesRepo = citiesRepo

    def create_city(self, city_data: CitySchema):
        city = City(
            name=city_data.name,
            state_id=city_data.state_id,
        )  # type: ignore

        return self.citiesRepo.create(city)

    def update_city(
        self, city_id: int, city_data: CitySchema
    ):
        city = City(
            id=city_id,
            name=city_data.name,
            state_id=city_data.state_id,
        )  # type: ignore

        return self.citiesRepo.update(city)

    def delete_city(self, city_id: int):
        city = self.citiesRepo.get_by_id(city_id)
        self.citiesRepo.delete(city)

    def get_city_by_id(self, city_id: int):
        return self.citiesRepo.get_by_id(city_id)

    def get_by_name(self, name: str):
        return self.citiesRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[City]:
        return self.citiesRepo.list(
            name, pageSize, startIndex
        )
