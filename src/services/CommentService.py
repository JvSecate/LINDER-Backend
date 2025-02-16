from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.CommentModel import Comment
from repositories.CommentRepository import CommentRepository
from schemas.pydantic.CommentSchema import CommentSchema


class CommentService:
    commentsRepo: CommentRepository

    def __init__(
        self, commentsRepo: CommentRepository = Depends()
    ):
        self.commentsRepo = commentsRepo

    def create_comment(self, comment_data: CommentSchema):
        comment = Comment(
            comment=comment_data.comment,
            job_id=comment_data.job_id,
            likes=comment_data.likes,
            unlikes=comment_data.unlikes,
        )

        return self.commentsRepo.create(comment)

    def update_comment(
        self, comment_id: int, comment_data: CommentSchema
    ):
        comment = Comment(
            id=comment_id,
            comment=comment_data.comment,
            job_id=comment_data.job_id,
            likes=comment_data.likes,
            unlikes=comment_data.unlikes,
        )

        return self.commentsRepo.update(comment)

    def delete_comment(self, comment_id: int):
        comment = self.commentsRepo.get_by_id(comment_id)
        self.commentsRepo.delete(comment)

    def get_comment_by_id(self, comment_id: int):
        return self.commentsRepo.get_by_id(comment_id)

    def get_by_name(self, name: str):
        return self.commentsRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Comment]:
        return self.commentsRepo.list(
            name, pageSize, startIndex
        )
