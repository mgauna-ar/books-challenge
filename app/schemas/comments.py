from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    body: str

class CommentCreate(CommentBase):
    user: str
    pass

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user: str
    creation_date: datetime = datetime.utcnow()
    modified_date: datetime | None = None
    book_id: int

    class Config:
        orm_mode = True

