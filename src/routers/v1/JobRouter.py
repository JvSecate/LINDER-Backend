from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from services.JobService import JobService
from schemas.pydantic.JobSchema import (
    JobSchema,
    JobSchemaPost,
)


JobRouter = APIRouter(prefix="/v1/jobs", tags=["job"])


@JobRouter.get(
    "/list", response_model=ApiResponse[list[JobSchema]]
)
async def list_jobs(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    jobService: JobService = Depends(),
):
    body: dict | JobSchema
    message: str

    if len(jobService.list(name, limit, start)) > 0:
        body = jobService.list(name, limit, start)  # type: ignore
        message = "List of Jobs"
        return ApiResponse[list[JobSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Jobs found"
        return ApiResponse[JobSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobRouter.post(
    "/create", response_model=ApiResponse[JobSchema]
)
async def create_job(
    job_data: JobSchemaPost,
    jobService: JobService = Depends(),
):
    body: dict | JobSchema
    message: str

    if jobService.get_by_name(job_data.title):
        message = "Job already exists"
        return ApiResponse[JobSchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = jobService.create_job(job_data)  # type: ignore
        message = "Job created"
        return ApiResponse[JobSchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@JobRouter.put(
    "/update/{id}", response_model=ApiResponse[JobSchema]
)
async def update_job(
    id: int,
    job_data: JobSchemaPost,
    jobService: JobService = Depends(),
):
    body: dict | JobSchema
    message: str

    if jobService.get_job_by_id(id):
        body = jobService.update_job(id, job_data)  # type: ignore
        message = "Job updated successfully"
        return ApiResponse[JobSchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Job not found"
        return ApiResponse[JobSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobRouter.delete("/delete/{id}")
async def delete_job(
    id: int,
    jobService: JobService = Depends(),
):
    message: str

    if jobService.get_job_by_id(id):
        jobService.delete_job(id)
        message = "Job deleted successfully"
        return ApiResponse[JobSchema](
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Job not found"
        return ApiResponse[JobSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
