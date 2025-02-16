from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from configs.Database import get_db_connection
from models.JobModel import Job


class JobRepository:
    """
    Repository class for managing Job objects in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, job: Job) -> Job:
        """
        Create a new job in the database.

        Args:
            job (Job): The job object to be created.

        Returns:
            Job: The created job object.
        """
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job: Job) -> Job | None:
        """
        Update an existing job in the database.

        Args:
            job (Job): The job object to be updated.

        Returns:
            Job | None: The updated job object, or None if the job does not exist.
        """
        self.db.merge(job)
        self.db.commit()

        return job

    def delete(self, job: Job) -> None:
        """
        Delete a job from the database.

        Args:
            job (Job): The job object to be deleted.

        Returns:
            None
        """
        self.db.delete(job)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Job]:
        """
        Retrieve a list of jobs from the database.

        Args:
            name (str): Optional. Filter jobs by name.
            limit (int): Optional. Limit the number of jobs to retrieve.
            start (int): Optional. Start index for pagination.

        Returns:
            List[Job]: The list of jobs matching the filter criteria.
        """
        query = self.db.query(Job)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Job:
        """
        Retrieve a job by its ID.

        Args:
            id (int): The ID of the job.

        Returns:
            Job: The job object with the specified ID.
        """
        return self.db.query(Job).get(id)

    def get_by_name(self, name: str) -> Job:
        """
        Retrieve a job by its name.

        Args:
            name (str): The name of the job.

        Returns:
            Job: The job object with the specified name.
        """
        return self.db.query(Job).filter_by(name=name).all()

    def get_all(self) -> List[Job]:
        """
        Retrieve all jobs from the database.

        Returns:
            List[Job]: The list of all jobs in the database.
        """
        return self.db.query(Job).all()
