from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.JobCategoryModel import JobCategory
from repositories.JobCategoryRepository import (
    JobCategoryRepository,
)
from schemas.pydantic.JobCategorySchema import (
    JobCategorySchema,
)


class JobCategoryService:
    jobCategoryRepo: JobCategoryRepository

    def __init__(
        self,
        jobCategoryRepo: JobCategoryRepository = Depends(),
    ):
        self.jobCategoryRepo = jobCategoryRepo

    def create_job_category(
        self, jobCategory_data: JobCategorySchema
    ):
        jobCategory = JobCategory(
            name=jobCategory_data.name,
        )

        return self.jobCategoryRepo.create(jobCategory)

    def update_job_category(
        self,
        jobCategory_id: int,
        jobCategory_data: JobCategorySchema,
    ):
        jobCategory = JobCategory(
            id=jobCategory_id,
            name=jobCategory_data.name,
        )

        return self.jobCategoryRepo.update(jobCategory)

    def delete_job_category(self, jobCategory_id: int):
        jobCategory = self.jobCategoryRepo.get_by_id(
            jobCategory_id
        )
        self.jobCategoryRepo.delete(jobCategory)

    def get_job_category_by_id(self, jobCategory_id: int):
        return self.jobCategoryRepo.get_by_id(
            jobCategory_id
        )

    def get_by_name(self, name: str):
        return self.jobCategoryRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[JobCategory]:
        return self.jobCategoryRepo.list(
            name, pageSize, startIndex
        )
