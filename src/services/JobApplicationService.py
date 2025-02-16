from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.JobApplicationModel import JobApplication
from repositories.JobApplicationRepository import (
    JobApplicationRepository,
)
from schemas.pydantic.JobApplicationSchema import (
    JobApplicationSchema,
)


class JobApplicationService:
    jobApplicationRepo: JobApplicationRepository

    def __init__(
        self,
        jobApplicationRepo: JobApplicationRepository = Depends(),
    ):
        self.jobApplicationRepo = jobApplicationRepo

    def create_job_application(
        self, job_application_data: JobApplicationSchema
    ):
        job_application = JobApplication(
            job_id=job_application_data.job_id,
            user_id=job_application_data.user_id,
        )

        return self.jobApplicationRepo.create(
            job_application
        )

    def update_job_application(
        self,
        job_application_id: int,
        job_application_data: JobApplicationSchema,
    ):
        job_application = JobApplication(
            id=job_application_id,
            job_id=job_application_data.job_id,
            user_id=job_application_data.user_id,
        )

        return self.jobApplicationRepo.update(
            job_application
        )

    def delete_job_application(
        self, job_application_id: int
    ):
        job_application = self.jobApplicationRepo.get_by_id(
            job_application_id
        )
        self.jobApplicationRepo.delete(job_application)

    def get_job_application_by_id(
        self, job_application_id: int
    ):
        return self.jobApplicationRepo.get_by_id(
            job_application_id
        )

    def get_by_name(self, name: str):
        return self.jobApplicationRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[JobApplication]:
        return self.jobApplicationRepo.list(
            name, pageSize, startIndex
        )
