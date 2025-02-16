from pydantic import BaseModel

class CommentSchemaPost(BaseModel):
    comment: str
    job_id: int
    likes: int
    unlikes: int

    class Config:
        from_attributes = True

class CommentSchema(CommentSchemaPost):
    id : int

    class Config:
        from_attributes = True