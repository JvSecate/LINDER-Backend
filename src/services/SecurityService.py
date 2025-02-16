from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from repositories.UserRepository import UserRepository

from schemas.pydantic.TokenData import TokenData


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str, hashed_password: str
):
    return pwd_context.verify(
        plain_password, hashed_password
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    userRepository: UserRepository = Depends(),
):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")  # type: ignore
        if email is None:
            raise ValueError("Invalid token")
        token_data = TokenData(username=email)  # type: ignore
    except JWTError:
        raise ValueError("Invalid token")

    user = userRepository.get_by_email(
        token_data.username  # type: ignore
    )

    if not user:
        raise ValueError("Invalid token")

    return user
