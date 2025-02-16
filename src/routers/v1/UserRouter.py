from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from models.UserModel import User
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.Token import Token
from schemas.pydantic.UserSchema import (
    UserSchema,
    UserPostSchema,
)
from services.SecurityService import (
    get_current_user,
)
from services.UserService import UserService

UserRouter = APIRouter(prefix="/v1/users", tags=["user"])


@UserRouter.get(
    "/list", response_model=ApiResponse[list[UserSchema]]
)
async def list_users(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    userService: UserService = Depends(),
):
    body: dict | User
    message: str

    if len(userService.list(name, limit, start)) > 0:
        body = userService.list(name, limit, start)  # type: ignore
        message = "List of users"
        return ApiResponse[list[UserSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No users found"
        return ApiResponse[UserSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@UserRouter.get(
    "/id/{user_id}", response_model=ApiResponse[UserSchema]
)
def get_user_by_id(
    user_id: int, userService: UserService = Depends()
):
    body: dict | UserSchema
    message: str

    if userService.get_user_by_id(user_id):
        body = userService.get_user_by_id(
            user_id
        ).normalize()
        message = "User found"
        return ApiResponse[UserSchema](
            body=body,
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "User not found"
        return ApiResponse[UserSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@UserRouter.get(
    "/me", response_model=ApiResponse[UserSchema]
)
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    body: dict | UserSchema
    message: str

    if current_user:
        body = current_user.normalize()
        message = "User found"
        return ApiResponse[UserSchema](
            body=body,
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "User not found"
        return ApiResponse[UserSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@UserRouter.get(
    "/email/{email}", response_model=ApiResponse[UserSchema]
)
async def get_user_by_email(
    email, userService: UserService = Depends()
):
    body: dict | UserSchema
    message: str

    if userService.get_user_by_email("%" + email + "%"):
        body = userService.get_user_by_email(
            "%" + email + "%"
        )  # type: ignore

        if body is None:
            message = "User not found"
            return ApiResponse[UserSchema](
                message=message,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            message = "User found"
            return ApiResponse[UserSchema](
                body=body,
                message=message,
                status_code=status.HTTP_200_OK,
            )
    else:
        message = "User not found"
        return ApiResponse[UserSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@UserRouter.post(
    "/create/",
    response_model=ApiResponse[UserSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserPostSchema,
    res: Response,
    userService: UserService = Depends(),
):
    body: dict | UserSchema
    message: str

    if userService.get_user_by_email(user.email):
        res.status_code = status.HTTP_409_CONFLICT
        message = "Email already exists"
        return ApiResponse[UserSchema](
            message=message,
            status_code=res.status_code,
        )
    else:
        res.status_code = status.HTTP_201_CREATED
        message = "User created successfully"
        body = userService.create_user(user).normalize()  # type: ignore
        return ApiResponse[UserSchema](
            body=body,
            message=message,
            status_code=res.status_code,
        )


@UserRouter.post(
    "/token", response_model=ApiResponse[Token]
)
async def login_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    userService: UserService = Depends(),
):
    user = userService.get_user_by_email(form_data.username)

    if not user:
        return ApiResponse[Token](
            message="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not userService.verify_password(form_data.password, user.password):  # type: ignore
        return ApiResponse[Token](
            message="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token = userService.create_access_token(data={"sub": user.email})  # type: ignore

    return ApiResponse[Token](
        message="Login successful",
        body={
            "access_token": access_token,
            "token_type": "Bearer",
        },
        status_code=status.HTTP_200_OK,
    )  # type: ignore


@UserRouter.put(
    "/update/{user_id}",
    response_model=ApiResponse[UserSchema],
)
async def update_user(
    user_id: int,
    user: UserPostSchema,
    res: Response,
    userService: UserService = Depends(),
    current_user: User = Depends(get_current_user),
):
    body: dict | UserSchema
    message: str

    if bool(current_user.id != user_id):
        res.status_code = status.HTTP_401_UNAUTHORIZED
        message = "Unauthorized"
        return ApiResponse[UserSchema](
            message=message,
            status_code=res.status_code,
        )

    user = userService.update_user(user_id, user).normalize()  # type: ignore

    if user:
        res.status_code = status.HTTP_200_OK
        message = "User updated successfully"
        body = user  # type: ignore
        return ApiResponse[UserSchema](
            body=body,
            message=message,
            status_code=res.status_code,
        )


@UserRouter.delete(
    "/delete/{user_id}",
    response_model=ApiResponse[UserSchema],
)
async def delete_user(
    user_id: int,
    res: Response,
    userService: UserService = Depends(),
    current_user: User = Depends(get_current_user),
):
    message: str

    if bool(current_user.id != user_id):
        res.status_code = status.HTTP_401_UNAUTHORIZED
        message = "Unauthorized"
        return ApiResponse[UserSchema](
            message=message,
            status_code=res.status_code,
        )

    userService.delete_user(user_id)

    res.status_code = status.HTTP_200_OK
    message = "User deleted successfully"
    return ApiResponse[UserSchema](
        message=message,
        status_code=res.status_code,
    )
