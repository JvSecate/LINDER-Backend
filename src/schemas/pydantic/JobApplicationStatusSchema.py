from pydantic import BaseModel


class JobApplicationStatusSchema(BaseModel):
    job_id: int
    user_id: int

    class Config:
        orm_mode = True