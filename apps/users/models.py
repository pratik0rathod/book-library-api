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
    
from apps.books.models import Books