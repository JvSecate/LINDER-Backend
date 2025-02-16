from pydantic import BaseModel


class JobSchemaPost(BaseModel):
    title: str
    description: str
    salary: float
    company_id: int
    new: bool
    remote: bool
    fullTime: bool
    partTime: bool
    featured: bool
    skills_id: list[int] = []
    active: bool
    categories: list[int] = []

    class Config:
        from_attributes = True


class JobSchema(JobSchemaPost):
    id : int

    class Config:
        from_attributes = True