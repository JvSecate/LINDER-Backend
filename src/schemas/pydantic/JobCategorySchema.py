from pydantic import BaseModel


class JobCategoryPostSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class JobCategorySchema(JobCategoryPostSchema):
    id: int

    class Config:
        from_attributes = True
