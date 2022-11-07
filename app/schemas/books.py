from pydantic import BaseModel
from app.schemas.comments import Comment

class BookBase(BaseModel):
    isbn: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    information: str
    comments: list[Comment] = []

    class Config:
        orm_mode = True