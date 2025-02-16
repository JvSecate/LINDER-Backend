from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.StateModel import State


class StateRepository:
    """
    Repository class for managing states in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        """
        Initializes a new instance of the StateRepository class.

        Args:
            db (Session): The database session to use. Defaults to the result of get_db_connection.
        """
        self.db = db

    def create(self, state: State) -> State:
        """
        Creates a new state in the database.

        Args:
            state (State): The state object to create.

        Returns:
            State: The created state object.
        """
        self.db.add(state)
        self.db.commit()
        self.db.refresh(state)
        return state

    def update(self, state: State) -> State | None:
        """
        Updates an existing state in the database.

        Args:
            state (State): The state object to update.

        Returns:
            State | None: The updated state object, or None if the state does not exist.
        """
        self.db.merge(state)
        self.db.commit()

        return state

    def delete(self, state: State) -> None:
        """
        Deletes a state from the database.

        Args:
            state (State): The state object to delete.
        """
        self.db.delete(state)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[State]:
        """
        Retrieves a list of states from the database.

        Args:
            name (str): The name of the state to filter by. Defaults to None.
            limit (int): The maximum number of states to retrieve. Defaults to None.
            start (int): The index of the first state to retrieve. Defaults to None.

        Returns:
            List[State]: A list of state objects.
        """
        query = self.db.query(State)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> State:
        """
        Retrieves a state by its ID.

        Args:
            id (int): The ID of the state to retrieve.

        Returns:
            State: The state object.
        """
        return self.db.query(State).get(id)

    def get_by_name(self, name: str) -> State:
        """
        Retrieves a state by its name.

        Args:
            name (str): The name of the state to retrieve.

        Returns:
            State: The state object.
        """
        return (
            self.db.query(State).filter_by(name=name).all()
        )

    def get_all(self) -> List[State]:
        """
        Retrieves all states from the database.

        Returns:
            List[State]: A list of state objects.
        """
        return self.db.query(State).all()
