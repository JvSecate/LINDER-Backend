from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from configs.Database import get_db_connection
from models.CountryModel import Country


class CountryRepository:
    """
    Repository class for managing Country objects in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        """
        Initializes a new instance of the CountryRepository class.

        Args:
            db (Session): The database session to use. Defaults to the result of the get_db_connection function.
        """
        self.db = db

    def create(self, country: Country) -> Country:
        """
        Creates a new country in the database.

        Args:
            country (Country): The country object to create.

        Returns:
            Country: The created country object.
        """
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)
        return country

    def update(self, country: Country) -> Country | None:
        """
        Updates an existing country in the database.

        Args:
            country (Country): The country object to update.

        Returns:
            Country | None: The updated country object, or None if the country was not found.
        """
        self.db.merge(country)
        self.db.commit()

        return country

    def delete(self, country: Country) -> None:
        """
        Deletes a country from the database.

        Args:
            country (Country): The country object to delete.
        """
        self.db.delete(country)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Country]:
        """
        Retrieves a list of countries from the database.

        Args:
            name (str): The name of the country to filter by. Defaults to None.
            limit (int): The maximum number of countries to retrieve. Defaults to None.
            start (int): The index of the first country to retrieve. Defaults to None.

        Returns:
            List[Country]: A list of country objects.
        """
        query = self.db.query(Country)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Country:
        """
        Retrieves a country by its ID from the database.

        Args:
            id (int): The ID of the country to retrieve.

        Returns:
            Country: The country object.
        """
        return self.db.query(Country).get(id)

    def get_by_name(self, name: str) -> Country:
        """
        Retrieves a list of countries by their name from the database.

        Args:
            name (str): The name of the countries to retrieve.

        Returns:
            List[Country]: A list of country objects.
        """
        return (
            self.db.query(Country)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[Country]:
        """
        Retrieves all countries from the database.

        Returns:
            List[Country]: A list of country objects.
        """
        return self.db.query(Country).all()
