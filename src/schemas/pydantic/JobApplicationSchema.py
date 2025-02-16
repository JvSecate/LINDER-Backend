from pydantic import BaseModel


class JobApplicationSchemaPost(BaseModel):
    job_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True


class JobApplicationSchema(JobApplicationSchemaPost):
    id: int

    class Config:
        from_attributes = True
