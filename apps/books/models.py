from . import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship,backref
from typing import Optional
from datetime import date,timedelta

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

class Books(base.Base):
    __tablename__ = "books"
    
    title:Mapped[str]
    isbn:Mapped[str]
    author:Mapped[str]
    synopsis:Mapped[Optional[str]] 
    genre = mapped_column(ARRAY(String),nullable=True)
    is_available: Mapped[bool] = mapped_column(default=True)
    publication_date:Mapped[date] 
    ratings:Mapped[float]
    added_by:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=True)
    added_by_user = relationship("Users", back_populates="added_books")
    book_transaction = relationship("BookTransaction",back_populates="book")
    
class BookTransaction(base.Base):
    __tablename__ = "book_transaction"
    
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id:Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrow_date:Mapped[date] = mapped_column(default=date.today())
    due_date:Mapped[date] = mapped_column(default=(date.today()+timedelta(30)))
    return_date:Mapped[date] = mapped_column(nullable=True)
    
    user =relationship("Users", back_populates="book_transaction")
    book =relationship("Books", back_populates="book_transaction")
    
    
from apps.users.models import Users
