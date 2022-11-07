from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.books import Book 

class CRUDBook():
    def __init__(self):
        """
        CRUD object with methods to Create, Read, Update, Delete (CRUD) Books.
        """
        pass
    
    def get(self, db: Session, book_id: int) -> Book | None:
        return db.query(Book).filter(Book.Book.id == book_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Book] | None:
        return db.query(Book).offset(skip).limit(limit).all()

    def get_by_isbn(self, db: Session, isbn: str) -> Book | None:
        return db.query(Book).filter(Book.isbn == isbn).first()

    def create(self, db: Session, isbn: str, information: str) -> Book | None:
        db_book = Book(isbn=isbn, information=information)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def update(self, db: Session, db_book: Book, information: str) -> Book | None:
        db_book.information = information
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def remove(self, db: Session, book_id: int) -> Book | None:
        db_book = db.query(Book).get(book_id)
        db.delete(db_book)
        db.commit()
        return db_book

book = CRUDBook()