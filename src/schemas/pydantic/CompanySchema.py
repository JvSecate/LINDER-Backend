from pydantic import BaseModel


class CompanyPostSchema(BaseModel):
    name: str
    website: str
    email: str
    description: str
    location_id: str | int | None = None
    active: bool

    class Config:
        from_attributes = True


class CompanySchema(CompanyPostSchema):
    id: int

    class Config:
        from_attributes = True