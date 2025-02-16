from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.JobApplicationStatusSchema import (
    JobApplicationStatusSchema,
)
from services.JobApplicationStatusService import (
    JobApplicationStatusService,
)

JobApplicationStatusRouter = APIRouter(
    prefix="/v1/job-application-statuses",
    tags=["job-application-status"],
)


@JobApplicationStatusRouter.get(
    "/list",
    response_model=ApiResponse[
        list[JobApplicationStatusSchema]
    ],
)
async def list_job_application_statuses(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    jobApplicationStatusService: JobApplicationStatusService = Depends(),
):
    body: dict | JobApplicationStatusSchema
    message: str

    if (
        len(
            jobApplicationStatusService.list(
                name, limit, start
            )
        )
        > 0
    ):
        body = jobApplicationStatusService.list(name, limit, start)  # type: ignore
        message = "List of Job Application Statuses"
        return ApiResponse[
            list[JobApplicationStatusSchema]
        ](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Job Application Statuses found"
        return ApiResponse[JobApplicationStatusSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobApplicationStatusRouter.post(
    "/create",
    response_model=ApiResponse[JobApplicationStatusSchema],
)
async def create_job_application_status(
    jobApplicationStatus_data: JobApplicationStatusSchema,
    jobApplicationStatusService: JobApplicationStatusService = Depends(),
):
    body: dict | JobApplicationStatusSchema
    message: str

    jobApplicationStatusService.create_job_application_status(jobApplicationStatus_data)  # type: ignore
    message = "Job Application Status created"
    return ApiResponse[JobApplicationStatusSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


@JobApplicationStatusRouter.put(
    "/update/{id}",
    response_model=ApiResponse[JobApplicationStatusSchema],
)
async def update_job_application_status(
    id: int,
    jobApplicationStatus_data: JobApplicationStatusSchema,
    jobApplicationStatusService: JobApplicationStatusService = Depends(),
):
    body: dict | JobApplicationStatusSchema
    message: str

    if jobApplicationStatusService.get_job_application_status_by_id(
        id
    ):
        body = jobApplicationStatusService.update_job_application_status(
            id, jobApplicationStatus_data
        )
        message = "Job Application Status updated"
        return ApiResponse[JobApplicationStatusSchema](
            body=body,
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Job Application Status not found"
        return ApiResponse[JobApplicationStatusSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@JobApplicationStatusRouter.delete(
    "/delete/{id}",
    response_model=ApiResponse[JobApplicationStatusSchema],
)
async def delete_job_application_status(
    id: int,
    jobApplicationStatusService: JobApplicationStatusService = Depends(),
):
    message: str

    if jobApplicationStatusService.get_job_application_status_by_id(
        id
    ):
        jobApplicationStatusService.delete_job_application_status(
            id
        )
        message = "Job Application Status deleted"
        return ApiResponse[JobApplicationStatusSchema](
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Job Application Status not found"
        return ApiResponse[JobApplicationStatusSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
