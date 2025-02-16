from pydantic import BaseModel

from schemas.pydantic.CitySchema import CitySchema


class StatePostSchema(BaseModel):
    name: str
    initials: str
    cities: list[CitySchema] = []
    country_id: int

    class Config:
        from_attributes = True


class StateSchema(StatePostSchema):
    id: int

    class Config:
        from_attributes = True
