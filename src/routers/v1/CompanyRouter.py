from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.CompanySchema import (
    CompanyPostSchema,
    CompanySchema,
)
from services.CompanyService import CompanyService

CompanyRouter = APIRouter(
    prefix="/v1/companies", tags=["company"]
)


@CompanyRouter.get(
    "/list", response_model=ApiResponse[list[CompanySchema]]
)
async def list_companies(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    companyService: CompanyService = Depends(),
):
    body: dict | CompanySchema
    message: str

    if len(companyService.list(name, limit, start)) > 0:
        body = companyService.list(name, limit, start)  # type: ignore
        message = "List of Companies"
        return ApiResponse[list[CompanySchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Companies found"
        return ApiResponse[CompanySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@CompanyRouter.post(
    "/create", response_model=ApiResponse[CompanySchema]
)
async def create_company(
    company_data: CompanyPostSchema,
    companyService: CompanyService = Depends(),
):
    body: dict | CompanySchema
    message: str

    if companyService.get_by_name(company_data.name):
        message = "Company already exists"
        return ApiResponse[CompanySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = companyService.create_company(company_data)  # type: ignore
        message = "Company created"
        return ApiResponse[CompanySchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@CompanyRouter.put(
    "/update/{id}",
    response_model=ApiResponse[CompanySchema],
)
async def update_company(
    id: int,
    company_data: CompanyPostSchema,
    companyService: CompanyService = Depends(),
):
    body: dict | CompanySchema
    message: str

    if companyService.get_company_by_id(id):
        body = companyService.update_company(id, company_data)  # type: ignore
        message = "Company updated"
        return ApiResponse[CompanySchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "Company not found"
        return ApiResponse[CompanySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@CompanyRouter.delete("/delete/{id}")
async def delete_company(
    id: int,
    companyService: CompanyService = Depends(),
):
    message: str

    if companyService.get_company_by_id(id):
        companyService.delete_company(id)  # type: ignore
        message = "Company deleted"
        return ApiResponse[CompanySchema](
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "Company not found"
        return ApiResponse[CompanySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
