from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.CityModel import City


class CityRepository:
    """
    Repository class for managing City objects in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        """
        Initializes a new instance of the CityRepository class.

        Args:
            db (Session): The database session to use. Defaults to the result of the get_db_connection function.
        """
        self.db = db

    def create(self, city: City) -> City:
        """
        Creates a new city in the database.

        Args:
            city (City): The city object to create.

        Returns:
            City: The created city object.
        """
        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)
        return city

    def update(self, city: City) -> City | None:
        """
        Updates an existing city in the database.

        Args:
            city (City): The city object to update.

        Returns:
            City | None: The updated city object, or None if the city was not found.
        """
        self.db.merge(city)
        self.db.commit()

        return city

    def delete(self, city: City) -> None:
        """
        Deletes a city from the database.

        Args:
            city (City): The city object to delete.
        """
        self.db.delete(city)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[City]:
        """
        Retrieves a list of cities from the database.

        Args:
            name (str | None): The name of the city to filter by. Defaults to None.
            limit (int | None): The maximum number of cities to retrieve. Defaults to None.
            start (int | None): The index of the first city to retrieve. Defaults to None.

        Returns:
            List[City]: The list of cities that match the specified criteria.
        """
        query = self.db.query(City)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> City:
        """
        Retrieves a city by its ID.

        Args:
            id (int): The ID of the city to retrieve.

        Returns:
            City: The city object with the specified ID.
        """
        return self.db.query(City).get(id)

    def get_by_name(self, name: str) -> City:
        """
        Retrieves a list of cities by their name.

        Args:
            name (str): The name of the cities to retrieve.

        Returns:
            List[City]: The list of cities with the specified name.
        """
        return (
            self.db.query(City).filter_by(name=name).all()
        )

    def get_all(self) -> List[City]:
        """
        Retrieves all cities from the database.

        Returns:
            List[City]: The list of all cities in the database.
        """
        return self.db.query(City).all()
