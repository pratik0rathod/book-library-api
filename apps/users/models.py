from . import base

from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Enum
from datetime import date
import enum

class UserEnum(enum.Enum):
    ADMIN = 'ADMIN'
    READER = 'READER'
    LIBRARIAN = 'LIBRARIAN'

class Users(base.Base):
    __tablename__ = "users"
    
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
    user_type:Mapped[UserEnum] = mapped_column(default=UserEnum.READER)    
    birth_date:Mapped[date]
    is_active : Mapped[bool] = mapped_column(default=True)
    added_by_admin :Mapped[bool] = mapped_column(default=False)
    soft_delete:Mapped[bool] = mapped_column(default=False,nullable=True)
    
    added_books = relationship("Books", back_populates="added_by_user")
    book_transaction = relationship("BookTransaction",back_populates="user")
    
from apps.books.models import Books

