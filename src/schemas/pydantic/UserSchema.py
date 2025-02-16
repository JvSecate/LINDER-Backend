from pydantic import BaseModel


class UserPostSchema(BaseModel):
    name: str
    email: str
    phone: str
    profile: str | None
    experience: str | None
    password: str

    class Config:
        from_attributes = True


class UserSchema(UserPostSchema):
    id: int

    class Config:
        from_attributes = True
