from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.JobApplicationStatusModel import JobApplicationStatus
from repositories.JobApplicationStatusRepository import (
    JobApplicationStatusRepository,
)
from schemas.pydantic.JobApplicationStatusSchema import (
    JobApplicationStatusSchema,
)


class JobApplicationStatusService:
    jobApplicationStatusRepo: JobApplicationStatusRepository

    def __init__(
        self,
        jobApplicationStatusRepo: JobApplicationStatusRepository = Depends(),
    ):
        self.jobApplicationStatusRepo = jobApplicationStatusRepo

    def create_job_application_status(
        self, job_application_data: JobApplicationStatusSchema
    ):
        job_application = JobApplicationStatus(
            job_id=job_application_data.job_id,
            user_id=job_application_data.user_id,
        )

        return self.jobApplicationStatusRepo.create(
            job_application
        )

    def update_job_application_status(
        self,
        job_application_id: int,
        job_application_data: JobApplicationStatusSchema,
    ):
        job_application = JobApplicationStatus(
            id=job_application_id,
            job_id=job_application_data.job_id,
            user_id=job_application_data.user_id,
        )

        return self.jobApplicationStatusRepo.update(
            job_application
        )

    def delete_job_application_status(
        self, job_application_id: int
    ):
        job_application = self.jobApplicationStatusRepo.get_by_id(
            job_application_id
        )
        self.jobApplicationStatusRepo.delete(job_application)

    def get_job_application_status_by_id(
        self, job_application_id: int
    ):
        return self.jobApplicationStatusRepo.get_by_id(
            job_application_id
        )

    def get_by_name(self, name: str):
        return self.jobApplicationStatusRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[JobApplicationStatus]:
        return self.jobApplicationStatusRepo.list(
            name, pageSize, startIndex
        )
