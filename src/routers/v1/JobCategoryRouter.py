from typing import List, Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.JobCategorySchema import (
    JobCategorySchema,
    JobCategoryPostSchema,
)
from services.JobCategoryService import JobCategoryService

JobCategoryRouter = APIRouter(
    prefix="/v1/job-categories", tags=["job-category"]
)


@JobCategoryRouter.get(
    "/list",
    response_model=ApiResponse[list[JobCategorySchema]],
)
async def list_job_categories(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    jobCategoryService: JobCategoryService = Depends(),
):
    body: dict | List[JobCategorySchema]
    message: str

    body = jobCategoryService.list(name, limit, start)  # type: ignore
    if len(body) > 0:
        message = "List of Job Categories"
        return ApiResponse[list[JobCategorySchema]](
            body=body,
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Job Categories found"
        body = []
        return ApiResponse[JobCategorySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobCategoryRouter.post(
    "/create", response_model=ApiResponse[JobCategorySchema]
)
async def create_job_category(
    jobCategory_data: JobCategoryPostSchema,
    jobCategoryService: JobCategoryService = Depends(),
):
    body: dict | JobCategorySchema
    message: str

    if jobCategoryService.get_by_name(
        jobCategory_data.name
    ):
        message = "Job Category already exists"
        return ApiResponse[JobCategorySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = jobCategoryService.create_job_category(jobCategory_data)  # type: ignore
        message = "Job Category created"
        return ApiResponse[JobCategorySchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@JobCategoryRouter.put(
    "/update/{id}",
    response_model=ApiResponse[JobCategorySchema],
)
async def update_job_category(
    id: int,
    jobCategory_data: JobCategoryPostSchema,
    jobCategoryService: JobCategoryService = Depends(),
):
    body: dict | JobCategorySchema
    message: str

    if jobCategoryService.get_job_category_by_id(id):
        body = jobCategoryService.update_job_category(id, jobCategory_data)  # type: ignore
        message = "Job Category updated"
        return ApiResponse[JobCategorySchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "Job Category not found"
        return ApiResponse[JobCategorySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobCategoryRouter.delete("/delete/{id}")
async def delete_job_category(
    id: int,
    jobCategoryService: JobCategoryService = Depends(),
):
    message: str

    if jobCategoryService.get_job_category_by_id(id):
        jobCategoryService.delete_job_category(id)
        message = "Job Category deleted"
        return ApiResponse[JobCategorySchema](
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "Job Category not found"
        return ApiResponse[JobCategorySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
