from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.CountrySchema import (
    CountrySchema,
    CountryPostSchema,
)
from services.CountryService import CountryService


CountryRouter = APIRouter(
    prefix="/v1/countries", tags=["country"]
)


@CountryRouter.get(
    "/list", response_model=ApiResponse[list[CountrySchema]]
)
async def list_countries(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    countryService: CountryService = Depends(),
):
    body: dict | CountrySchema
    message: str

    if len(countryService.list(name, limit, start)) > 0:
        body = countryService.list(name, limit, start)  # type: ignore
        message = "List of Countries"
        return ApiResponse[list[CountrySchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Countries found"
        return ApiResponse[CountrySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@CountryRouter.post(
    "/create", response_model=ApiResponse[CountrySchema]
)
async def create_country(
    country_data: CountryPostSchema,
    countryService: CountryService = Depends(),
):
    body: dict | CountrySchema
    message: str

    if countryService.get_by_name(name=country_data.name):
        message = "Country already exists"
        return ApiResponse[CountrySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = countryService.create_country(country_data=country_data)  # type: ignore
        message = "Country created successfully"
        return ApiResponse[CountrySchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@CountryRouter.put(
    "/update/{state_id}",
    response_model=ApiResponse[CountrySchema],
)
async def update_country(
    state_id: int,
    country_data: CountryPostSchema,
    countryService: CountryService = Depends(),
):
    body: dict | CountrySchema
    message: str

    if countryService.get_country_by_id(state_id):
        body = countryService.update_country(id=state_id, country_data=country_data)  # type: ignore
        message = "Country updated successfully"
        return ApiResponse[CountrySchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_202_ACCEPTED,
        )
    else:
        message = "Country already exists"
        return ApiResponse[CountrySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


@CountryRouter.delete("/delete/{state_id}")
async def delete_country(
    country_id: int,
    countryService: CountryService = Depends(),
):
    message: str

    if countryService.get_country_by_id(country_id):
        countryService.delete_country(country_id)
        message = "Country deleted successfully"
        return ApiResponse[CountrySchema](
            message=message,
            status_code=status.HTTP_202_ACCEPTED,
        )
    else:
        message = "Country not found"
        return ApiResponse[CountrySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
