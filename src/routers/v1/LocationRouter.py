from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.LocationSchema import (
    LocationSchema,
    LocationPostSchema,
)
from services.LocationService import LocationService

LocationRouter = APIRouter(
    prefix="/v1/locations", tags=["location"]
)


@LocationRouter.get(
    "/list",
    response_model=ApiResponse[list[LocationSchema]],
)
async def list_locations(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    locationService: LocationService = Depends(),
):
    body: dict | LocationSchema
    message: str

    if len(locationService.list(name, limit, start)) > 0:
        body = locationService.list(name, limit, start)  # type: ignore
        message = "List of Locations"
        return ApiResponse[list[LocationSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Locations found"
        return ApiResponse[LocationSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@LocationRouter.post(
    "/create", response_model=ApiResponse[LocationSchema]
)
async def create_location(
    location_data: LocationPostSchema,
    locationService: LocationService = Depends(),
):
    body: dict | LocationSchema
    message: str

    if locationService.get_by_name(location_data.name):
        message = "Location already exists"
        return ApiResponse[LocationSchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = locationService.create_location(location_data)  # type: ignore
        message = "Location created"
        return ApiResponse[LocationSchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    
@LocationRouter.put("/update/{id}", response_model=ApiResponse[LocationSchema])
async def update_location(
    id: int,
    location_data: LocationPostSchema,
    locationService: LocationService = Depends(),
):
    body: dict | LocationSchema
    message: str

    if locationService.get_by_name(location_data.name):
        message = "Location already exists"
        return ApiResponse[LocationSchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = locationService.update_location(id, location_data)  # type: ignore
        message = "Location updated"
        return ApiResponse[LocationSchema](
            body=body,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )
    
@LocationRouter.delete("/delete/{id}")
async def delete_location(
    id: int,
    locationService: LocationService = Depends(),
):
    message: str

    if locationService.get_location_by_id(id):
        locationService.delete_location(id) 
        message = "Location deleted"
        return ApiResponse[LocationSchema](
            message=message,
            status_code=status.HTTP_200_OK,
        )
