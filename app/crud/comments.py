from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from app.models.comments import Comment
from app.models.books import Book
from app.schemas.comments import CommentCreate, CommentUpdate

class CRUDComment():
    def __init__(self):
        """
        CRUD object with methods to Create, Read, Update, Delete (CRUD) Comments.
        """
        pass

    def get(self, db: Session, comment_id: int) -> Comment | None:
        return db.query(Comment).filter(Comment.id == comment_id).first()

    def get_all(self, db: Session, isbn: str, skip: int = 0, limit: int = 100) -> list[Comment] | None:
        return db.query(Comment).join(Book).filter(Book.isbn == isbn ).offset(skip).limit(limit).all()

    def create(self, db: Session, db_book: Book, comment_in: CommentCreate) -> Comment | None:
        db_comment = Comment(**comment_in.dict())
        db_comment.book_id = db_book.id
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def update(self, db: Session, db_comment: Comment, comment_in: CommentUpdate) -> Comment | None:
        obj_data = jsonable_encoder(db_comment)
        update_data = comment_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_comment, field, update_data[field])
        db_comment.modified_date = datetime.utcnow()
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def remove(self, db: Session, comment_id: int) -> Comment | None:
        db_comment = db.query(Comment).get(comment_id)
        db.delete(db_comment)
        db.commit()
        return db_comment

comment = CRUDComment()