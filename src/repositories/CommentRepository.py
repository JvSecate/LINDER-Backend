from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from configs.Database import get_db_connection
from models.CommentModel import Comment


class CommentRepository:
    """
    Repository class for managing comments in the database.
    """

    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        """
        Initializes a new instance of the CommentRepository class.

        Args:
            db (Session): The database session to use.
        """
        self.db = db

    def create(self, comment: Comment) -> Comment:
        """
        Creates a new comment in the database.

        Args:
            comment (Comment): The comment to create.

        Returns:
            Comment: The created comment.
        """
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: Comment) -> Comment | None:
        """
        Updates an existing comment in the database.

        Args:
            comment (Comment): The comment to update.

        Returns:
            Comment | None: The updated comment, or None if the comment does not exist.
        """
        self.db.merge(comment)
        self.db.commit()

        return comment

    def delete(self, comment: Comment) -> None:
        """
        Deletes a comment from the database.

        Args:
            comment (Comment): The comment to delete.
        """
        self.db.delete(comment)
        self.db.commit()
        self.db.flush()

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Comment]:
        """
        Retrieves a list of comments from the database.

        Args:
            name (str): The name to filter the comments by.
            limit (int): The maximum number of comments to retrieve.
            start (int): The index to start retrieving comments from.

        Returns:
            List[Comment]: The list of comments.
        """
        query = self.db.query(Comment)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()  # type: ignore

    def get_by_id(self, id: int) -> Comment:
        """
        Retrieves a comment by its ID.

        Args:
            id (int): The ID of the comment to retrieve.

        Returns:
            Comment: The retrieved comment.
        """
        return self.db.query(Comment).get(id)

    def get_by_name(self, name: str) -> Comment:
        """
        Retrieves a comment by its name.

        Args:
            name (str): The name of the comment to retrieve.

        Returns:
            Comment: The retrieved comment.
        """
        return (
            self.db.query(Comment)
            .filter_by(name=name)
            .all()
        )

    def get_all(self) -> List[Comment]:
        """
        Retrieves all comments from the database.

        Returns:
            List[Comment]: The list of comments.
        """
        return self.db.query(Comment).all()
