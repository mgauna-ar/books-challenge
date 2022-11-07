from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base

class Comment(Base):
    __tablename__ = "book_comment"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    body = Column(String)
    created_date = Column(DateTime, index=True)
    modified_date = Column(DateTime, index=True)
    book_id = Column(Integer, ForeignKey("book.id"))

    book = relationship("Book", back_populates="comments")