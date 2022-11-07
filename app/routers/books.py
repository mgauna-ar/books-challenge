import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.schemas.books import Book
from app.crud.books import book
from app.dependencies import get_db, validate_isbn

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=list[Book])
def read_all(
    db: Session = Depends(get_db)
):
    """
    Retrieve all books in database.
    """
    return book.get_all(db)


@router.post("/{isbn}", response_model=Book)
def create(
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Create a new book on database
    """
    book_rsp = book.get_by_isbn(db, isbn)
    if book_rsp:
        raise HTTPException(
            status_code=400,
            detail="Book already exists.",
        )
    information = requests.get(settings.BOOKS_PROVIDER_URL.format( isbn = isbn))
    print(information)
    book_rsp = book.create(db, isbn, str(information.json()))
    return book_rsp

@router.put("/{isbn}", response_model=Book)
def update(
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Update book information on database
    """
    db_book = book.get_by_isbn(db, isbn)
    if not db_book:
        raise HTTPException(
            status_code=400,
            detail="Book doesn't exists.",
        ) 
    information = requests.get(settings.BOOKS_PROVIDER_URL.format( isbn = isbn))
    print(information)
    book_rsp = book.update(db, db_book, str(information.json()))
    return book_rsp

@router.get("/{isbn}", response_model=Book)
def read(
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Get book information from database
    """
    book_rsp = book.get_by_isbn(db, isbn)
    if not book_rsp:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_rsp

@router.delete("/{isbn}", response_model=Book)
def delete(
    isbn: str = Depends(validate_isbn),
    db: Session = Depends(get_db)
):
    """
    Delete comment from a book
    """
    db_book = book.get_by_isbn(db, isbn)
    if not db_book:
        raise HTTPException(
            status_code=400,
            detail="Comment doesn't exists.",
        )
    db_book = book.remove(db, db_book.id)
    return db_book

