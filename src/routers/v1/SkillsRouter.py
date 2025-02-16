from typing import List, Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.SkillsSchema import (
    SkillsSchema,
    SkillsSchemaPost,
)
from services.SkillsService import SkillsService

SkillsRouter = APIRouter(
    prefix="/v1/skills", tags=["skills"]
)


@SkillsRouter.get(
    "list", response_model=ApiResponse[list[SkillsSchema]]
)
async def list_skills(
    name: str,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    skillsService: SkillsService = Depends(),
):
    body: dict | List[SkillsSchema]
    message: str

    if len(skillsService.list(name, limit, start)) > 0:
        body = skillsService.list(name, limit, start)  # type: ignore
        message = "List of Skills"
        return ApiResponse[list[SkillsSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Skills found"
        return ApiResponse[SkillsSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@SkillsRouter.post(
    "/create", response_model=ApiResponse[SkillsSchema]
)
async def create_skills(
    skills_data: SkillsSchemaPost,
    skillsService: SkillsService = Depends(),
):
    body: dict | SkillsSchema
    message: str

    if skillsService.get_by_name(skills_data.name):
        message = "Skills already exists"
        return ApiResponse[SkillsSchema](
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
    else:
        body = skillsService.create(skills_data)  # type: ignore
        message = "Skills created"
        return ApiResponse[SkillsSchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_201_CREATED,
        )


@SkillsRouter.put(
    "/update/{id}", response_model=ApiResponse[SkillsSchema]
)
async def update_skills(
    id: int,
    skills_data: SkillsSchemaPost,
    skillsService: SkillsService = Depends(),
):
    body: dict | SkillsSchema
    message: str

    if skillsService.get_skills_by_id(id):
        body = skillsService.update_skills(id, skills_data)  # type: ignore
        message = "Skills updated"
        return ApiResponse[SkillsSchema](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Skills not found"
        return ApiResponse[SkillsSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@SkillsRouter.delete(
    "/delete/{id}", response_model=ApiResponse[SkillsSchema]
)
async def delete_skills(
    id: int,
    skillsService: SkillsService = Depends(),
):
    message: str

    if skillsService.get_skills_by_id(id):
        skillsService.delete_skills(id)
        message = "Skills deleted"
        return ApiResponse[SkillsSchema](
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "Skills not found"
        return ApiResponse[SkillsSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
