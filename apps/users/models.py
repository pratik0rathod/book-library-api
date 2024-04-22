from . import base

from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Enum
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
     
    # book:Mapped["Books"] =  relationship(back_populates="user")

from apps.books.models import Books