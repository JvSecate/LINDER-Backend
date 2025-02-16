from typing import Optional
from fastapi import APIRouter, Depends, status
from schemas.pydantic.ApiResponse import ApiResponse
from schemas.pydantic.CommentSchema import (
    CommentSchema,
    CommentSchemaPost,
)
from services.CommentService import CommentService


CommentRouter = APIRouter(
    prefix="/v1/comments", tags=["comment"]
)


@CommentRouter.get(
    "/list", response_model=ApiResponse[list[CommentSchema]]
)
async def list_comments(
    name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[int] = None,
    commentService: CommentService = Depends(),
):
    body: dict | CommentSchema
    message: str

    if len(commentService.list(name, limit, start)) > 0:
        body = commentService.list(name, limit, start)  # type: ignore
        message = "List of Comments"
        return ApiResponse[list[CommentSchema]](
            body=body,  # type: ignore
            message=message,
            status_code=status.HTTP_200_OK,
        )
    else:
        message = "No Comments found"
        return ApiResponse[CommentSchema](
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


@CommentRouter.post(
    "/create", response_model=ApiResponse[CommentSchema]
)
async def create_comment(
    comment_data: CommentSchemaPost,
    commentService: CommentService = Depends(),
):
    body: dict | CommentSchema
    message: str

    commentService.create_comment(comment_data)  # type: ignore
    message = "Comment created"
    return ApiResponse[CommentSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


@CommentRouter.put(
    "/update/{id}",
    response_model=ApiResponse[CommentSchema],
)
async def update_comment(
    id: int,
    comment_data: CommentSchemaPost,
    commentService: CommentService = Depends(),
):
    body: dict | CommentSchema
    message: str

    commentService.update_comment(id, comment_data)  # type: ignore
    message = "Comment updated"
    return ApiResponse[CommentSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


@CommentRouter.delete(
    "/delete/{id}",
    response_model=ApiResponse[CommentSchema],
)
async def delete_comment(
    id: int,
    commentService: CommentService = Depends(),
):
    message: str

    commentService.delete_comment(id)
    message = "Comment deleted"
    return ApiResponse[CommentSchema](
        message=message,
        status_code=status.HTTP_201_CREATED,
    )
