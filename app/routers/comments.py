from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.comments import Comment, CommentCreate, CommentUpdate
from app.crud.comments import comment
from app.crud.books import book
from app.dependencies import get_db, validate_isbn

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.get("/{isbn}", response_model=list[Comment])
def read_all(
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Retrieve all comments from a book.
    """
    return comment.get_all(db, isbn)


@router.post("/{isbn}", response_model=Comment)
def create( 
    comment_in: CommentCreate,
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Add new comment to a book
    """
    db_book = book.get_by_isbn(db, isbn)
    if not db_book:
        raise HTTPException(
            status_code=400,
            detail="Book doesn't exists.",
        )
    comment_rsp = comment.create(db, db_book, comment_in)
    return comment_rsp

@router.put("/{comment_id}", response_model=Comment)
def update(
    comment_id: int,
    comment_in: CommentUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update comment from a book
    """
    db_comment = comment.get(db, comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=400,
            detail="Comment doesn't exists.",
        )
    comment_rsp = comment.update(db, db_comment, comment_in)
    return comment_rsp

@router.delete("/{comment_id}", response_model=Comment)
def delete(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete comment from a book
    """
    db_comment = comment.get(db, comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=400,
            detail="Comment doesn't exists.",
        )
    db_comment = comment.remove(db, comment_id)
    return db_comment