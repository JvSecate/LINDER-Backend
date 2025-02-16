from typing import Optional
from fastapi import APIRouter, Depends, status
from models.StateModel import State

from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.StateSchema import (
    StateSchema,
    StatePostSchema,
)
from services.StateService import StateService


StateRouter = APIRouter(prefix="/v1/states", tags=["state"])


@StateRouter.get(
    "/list", response_model=ApiResponse[list[StateSchema]]
)
async def list_states(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    stateService: StateService = Depends(),
):
    body: dict | StateSchema
    message: str

    if len(stateService.list(name, limit, start)) > 0:
        body = stateService.list(name, limit, start)  # type: ignore
        message = "List of States"
        return ApiResponse[list[StateSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No States found"
        return ApiResponse[StateSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@StateRouter.post(
    "/create", response_model=ApiResponse[StateSchema]
)
async def create_state(
    state_data: StatePostSchema,
    stateService: StateService = Depends(),
):
    body: dict | StateSchema
    message: str

    if stateService.get_by_name(state_data.name):
        message = "State already exists"
        return ApiResponse[StateSchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = stateService.create_state(state_data=state_data)  # type: ignore
        message = "State created successfully"
        return ApiResponse[StateSchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@StateRouter.put(
    "/update/{state_id}",
    response_model=ApiResponse[StateSchema],
)
async def update_state(
    state_id: int,
    state_data: StatePostSchema,
    stateService: StateService = Depends(),
):
    body: dict | StateSchema
    message: str

    if stateService.get_state_by_id(state_id):
        body = stateService.update_state(
            state_id, state_data=state_data  # type: ignore
        )
        message = "State updated successfully"
        return ApiResponse[StateSchema](
            body=body,
            message=message,
            status_code=status.HTTP_202_ACCEPTED,
        )
    else:
        message = "State not found"
        return ApiResponse[StateSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@StateRouter.delete("/delete/{state_id}")
async def delete_state(
    state_id: int,
    stateService: StateService = Depends(),
):
    message: str

    if stateService.get_state_by_id(state_id):
        stateService.delete_state(state_id)
        message = "State deleted successfully"
        return ApiResponse[StateSchema](
            message=message,
            status_code=status.HTTP_202_ACCEPTED,
        )
    else:
        message = "State not found"
        return ApiResponse[StateSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
