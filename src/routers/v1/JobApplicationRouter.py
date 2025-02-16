from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.JobApplicationSchema import (
    JobApplicationSchema,
    JobApplicationSchemaPost,
)
from services.JobApplicationService import (
    JobApplicationService,
)

JobApplicationRouter = APIRouter(
    prefix="/v1/job-applications", tags=["job-application"]
)


@JobApplicationRouter.get(
    "list",
    response_model=ApiResponse[list[JobApplicationSchema]],
)
async def list_job_applications(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    jobApplicationService: JobApplicationService = Depends(),
):
    body: dict | JobApplicationSchema
    message: str

    if (
        len(jobApplicationService.list(name, limit, start))
        > 0
    ):
        body = jobApplicationService.list(name, limit, start)  # type: ignore
        message = "List of Job Applications"
        return ApiResponse[list[JobApplicationSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Job Applications found"
        return ApiResponse[JobApplicationSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobApplicationRouter.post(
    "/create",
    response_model=ApiResponse[JobApplicationSchema],
)
async def create_job_application(
    jobApplication_data: JobApplicationSchemaPost,
    jobApplicationService: JobApplicationService = Depends(),
):
    body: dict | JobApplicationSchema
    message: str

    jobApplicationService.create_job_application(jobApplication_data)  # type: ignore
    message = "Job Application created"
    return ApiResponse[JobApplicationSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


@JobApplicationRouter.put(
    "/update{id}",
    response_model=ApiResponse[JobApplicationSchema],
)
async def update_job_application(
    id: int,
    jobApplication_data: JobApplicationSchemaPost,
    jobApplicationService: JobApplicationService = Depends(),
):
    body: dict | JobApplicationSchema
    message: str

    jobApplicationService.update_job_application(id, jobApplication_data)  # type: ignore
    message = "Job Application updated"
    return ApiResponse[JobApplicationSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


@JobApplicationRouter.delete(
    "/delete{id}",
    response_model=ApiResponse[JobApplicationSchema],
)
async def delete_job_application(
    id: int,
    jobApplicationService: JobApplicationService = Depends(),
):
    message: str

    if jobApplicationService.get_job_application_by_id(id):
        jobApplicationService.delete_job_application(id) 
        message = "Job Application deleted"
        return ApiResponse[JobApplicationSchema](
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "Job Application not found"
        return ApiResponse[JobApplicationSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
