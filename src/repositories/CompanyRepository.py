from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.CompanyModel import Company


class CompanyRepository:
    """
    Repository class for managing Company entities in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, company: Company) -> Company:
        """
        Create a new company in the database.

        Args:
            company (Company): The company object to be created.

        Returns:
            Company: The created company object.
        """
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def update(self, company: Company) -> Company | None:
        """
        Update an existing company in the database.

        Args:
            company (Company): The company object to be updated.

        Returns:
            Company | None: The updated company object, or None if the company does not exist.
        """
        self.db.merge(company)
        self.db.commit()

        return company

    def delete(self, company: Company) -> None:
        """
        Delete a company from the database.

        Args:
            company (Company): The company object to be deleted.

        Returns:
            None
        """
        self.db.delete(company)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Company]:
        """
        Retrieve a list of companies from the database.

        Args:
            name (Optional[str]): Filter companies by name.
            limit (Optional[int]): Limit the number of results.
            start (Optional[int]): Start index for pagination.

        Returns:
            List[Company]: A list of company objects matching the specified criteria.
        """
        query = self.db.query(Company)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Company:
        """
        Retrieve a company by its ID.

        Args:
            id (int): The ID of the company.

        Returns:
            Company: The company object with the specified ID.
        """
        return self.db.query(Company).get(id)

    def get_by_name(self, name: str) -> Company:
        """
        Retrieve a list of companies by name.

        Args:
            name (str): The name of the company.

        Returns:
            List[Company]: A list of company objects with the specified name.
        """
        return (
            self.db.query(Company)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[Company]:
        """
        Retrieve all companies from the database.

        Returns:
            List[Company]: A list of all company objects.
        """
        return self.db.query(Company).all()
