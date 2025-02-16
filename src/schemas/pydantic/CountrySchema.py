from pydantic import BaseModel


class CountryPostSchema(BaseModel):
    name: str
    initials: str

    class Config:
        from_attributes = True


class CountrySchema(CountryPostSchema):
    id: int

    class Config:
        from_attributes = True
