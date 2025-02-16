from pydantic import BaseModel


class CityPostSchema(BaseModel):
    name: str
    state_id: int

    class Config:
        from_attributes = True


class CitySchema(CityPostSchema):
    id: int

    class Config:
        from_attributes = True
