from pydantic import BaseModel

class SkillsSchemaPost(BaseModel):
    name: str

    class Config:
        from_attributes = True

class SkillsSchema(SkillsSchemaPost):
    id : int

    class Config:
        from_attributes = True