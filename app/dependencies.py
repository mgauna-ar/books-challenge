from fastapi import HTTPException

from app.db.session import SessionLocal

def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_isbn(isbn: str):
    if len(isbn) == 13 and isbn.isdigit():
    #ISBN 13: The ISBN-13 check digit, which is the last digit of the ISBN, must range from 0 to 9 and must be such that the sum of all the thirteen digits, 
    #each multiplied by its (integer) weight, alternating between 1 and 3, is a multiple of 10.
        result = 0
        result = (sum(int(ch) for ch in isbn[::2]) + sum(int(ch) * 3 for ch in isbn[1::2]))
        if result % 10 != 0:
            raise HTTPException(status_code=400, detail="ISBN is not valid")
    else:
        raise HTTPException(status_code=400, detail="ISBN must be 13 digits")
    return isbn
