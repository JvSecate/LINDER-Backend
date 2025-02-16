from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse

from schemas.pydantic.CitySchema import (
    CitySchema,
    CityPostSchema,
)

from services.CityService import CityService


CityRouter = APIRouter(prefix="/v1/cities", tags=["city"])


@CityRouter.get(
    "/list",
    response_model=ApiResponse[list[CitySchema]],
)
async def list_cities(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    cityService: CityService = Depends(),
):
    body: dict | CitySchema
    message: str

    if len(cityService.list(name, limit, start)) > 0:
        body = cityService.list(name, limit, start)  # type: ignore
        message = "List of cities"
        return ApiResponse[list[CitySchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No cities found"
        return ApiResponse[CitySchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@CityRouter.post(
    "/create", response_model=ApiResponse[CitySchema]
)
async def create_city(
    city_data: CityPostSchema,
    cityService: CityService = Depends(),
):
    body: dict | CitySchema
    message: str

    if cityService.get_by_name(name=city_data.name):
        message = "City already exists"
        return ApiResponse[CitySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = cityService.create_city(city_data=city_data)  # type: ignore
        message = "City created successfully"
        return ApiResponse[CitySchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@CityRouter.put(
    "/update/{city_id}",
    response_model=ApiResponse[CitySchema],
)
async def update_city(
    city_id: int,
    city_data: CityPostSchema,
    cityService: CityService = Depends(),
):
    body: dict | CitySchema
    message: str

    if cityService.get_city_by_id(city_id=city_id):
        message = "City already exists"
        return ApiResponse[CitySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = cityService.update_city(city_id=city_id, city_data=city_data)  # type: ignore
        message = "City updated successfully"
        return ApiResponse[CitySchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@CityRouter.delete(
    "/delete/{city_id}",
    response_model=ApiResponse[CitySchema],
)
async def delete_city(
    city_id: int,
    cityService: CityService = Depends(),
):
    message: str

    if cityService.get_city_by_id(city_id=city_id):
        cityService.delete_city(city_id=city_id)
        message = "City deleted successfully"
        return ApiResponse[CitySchema](
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    else:
        message = "City not found"
        return ApiResponse[CitySchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
