from typing import List, Optional
from fastapi import Depends
from models.CountryModel import Country
from repositories.CountryRepository import CountryRepository
from schemas.pydantic.CountrySchema import CountrySchema


class CountryService:
    CountriesRepo: CountryRepository

    def __init__(
        self, countriesRepo: CountryRepository = Depends()
    ):
        self.countriesRepo = countriesRepo

    def create_country(self, country_data: CountrySchema):
        country = Country(
            name=country_data.name,
        )  # type: ignore

        return self.countriesRepo.create(country)

    def update_country(
        self, country_id: int, country_data: CountrySchema
    ):
        country = Country(
            id=country_id,
            name=country_data.name,
            country_id=country_data,
        )  # type: ignore

        return self.countriesRepo.update(country)

    def delete_country(self, country_id: int):
        country = self.countriesRepo.get_by_id(country_id)
        self.countriesRepo.delete(country)

    def get_country_by_id(self, country_id: int):
        return self.countriesRepo.get_by_id(country_id)

    def get_by_name(self, name: str):
        return self.countriesRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Country]:
        return self.countriesRepo.list(
            name, pageSize, startIndex
        )
