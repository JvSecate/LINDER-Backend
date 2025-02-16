from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from configs.Database import (
    get_db_connection,
)
from models.UserModel import User


from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from models.UserModel import User
from configs.Database import get_db_connection


class UserRepository:
    """
    Repository class for handling CRUD operations on User objects.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        """
        Constructor method for UserRepository.

        Parameters:
        - db (Session): The database session to be used for database operations.
        """
        self.db = db

    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        Parameters:
        - user (User): The user object to be created.

        Returns:
        - User: The created user object.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User | None:
        """
        Update an existing user in the database.

        Parameters:
        - user (User): The user object to be updated.

        Returns:
        - User | None: The updated user object, or None if the user does not exist.
        """
        self.db.merge(user)
        self.db.commit()
        return user

    def delete(self, user: User) -> None:
        """
        Delete a user from the database.

        Parameters:
        - user (User): The user object to be deleted.
        """
        self.db.delete(user)
        self.db.commit()
        # self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[User]:
        """
        Retrieve a list of users from the database.

        Parameters:
        - name (Optional[str]): The name to filter the users by.
        - limit (Optional[int]): The maximum number of users to retrieve.
        - start (Optional[int]): The starting index of the users to retrieve.

        Returns:
        - List[User]: The list of retrieved users.
        """
        query = self.db.query(User)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all() # type: ignore

    def get_by_id(self, id: int) -> User:
        """
        Retrieve a user by their ID.

        Parameters:
        - id (int): The ID of the user to retrieve.

        Returns:
        - User: The retrieved user object.
        """
        return self.db.query(User).get(id)

    def get_by_name(self, name: str) -> User:
        """
        Retrieve users by their name.

        Parameters:
        - name (str): The name to search for.

        Returns:
        - User: The retrieved user object.
        """
        return (
            self.db.query(User)
            .filter(User.name.like(("%" + name + "%"))) # type: ignore
            .all()
        )

    def get_by_phone(self, phone: str) -> User:
        """
        Retrieve users by their phone number.

        Parameters:
        - phone (str): The phone number to search for.

        Returns:
        - User: The retrieved user object.
        """
        return (
            self.db.query(User)
            .filter(User.phone.like(("%" + phone + "%"))) # type: ignore
            .all()
        )

    def get_by_profile(self, profile: str) -> User:
        """
        Retrieve users by their profile.

        Parameters:
        - profile (str): The profile to search for.

        Returns:
        - User: The retrieved user object.
        """
        return (
            self.db.query(User)
            .filter_by(profile=profile)
            .all()
        )

    def get_by_email(self, email: str) -> User:
        """
        Retrieve users by their email.

        Parameters:
        - email (str): The email to search for.

        Returns:
        - User: The retrieved user object.
        """
        return (
            self.db.query(User) 
            .filter(User.email.like((email))) # type: ignore
            .first()
        )

    def get_all(self) -> List[User]:
        """
        Retrieve all users from the database.

        Returns:
        - List[User]: The list of retrieved users.
        """
        return self.db.query(User).all()
