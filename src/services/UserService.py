from typing import List, Optional
from fastapi import Depends
from models.UserModel import User

from repositories.UserRepository import UserRepository
from schemas.pydantic.UserSchema import (
    UserPostSchema,
    UserSchema,
)
from services.SecurityService import (
    get_password_hash,
    create_acess_token,
    verify_password,
)


class UserService:
    userRepository: UserRepository

    def __init__(
        self, userRepository: UserRepository = Depends()
    ) -> None:
        self.userRepository = userRepository

    def verify_password(
        self, plain_password, hashed_password
    ):
        return verify_password(
            hashed_password=hashed_password,
            plain_password=plain_password,
        )

    def create_access_token(self, data: dict):
        return create_acess_token(data)

    def create_user(self, user_data: UserSchema):
        hash_password = get_password_hash(
            user_data.password
        )

        user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            profile=user_data.profile,
            experience=user_data.experience,
            password=hash_password,
        )  # type: ignore

        return self.userRepository.create(user=user)

    def update_user(
        self, user_id: int, user_data: UserPostSchema
    ):
        password = get_password_hash(user_data.password)

        user = User(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            profile=user_data.profile,
            experience=user_data.experience,
            password=password,
        )  # type: ignore

        return self.userRepository.update(user=user)

    def delete_user(self, user_id):
        user = self.userRepository.get_by_id(user_id)
        if not user:
            return {}
        return self.userRepository.delete(user)

    def get_user_by_id(self, user_id):
        return self.userRepository.get_by_id(user_id)

    def get_user_by_email(self, email):
        if email is None:
            return {}

        if email == "" or email == " ":
            return {}

        return self.userRepository.get_by_email(email)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[User]:
        return self.userRepository.list(
            name, pageSize, startIndex
        )
