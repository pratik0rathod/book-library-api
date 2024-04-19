from . import base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Enum
import enum

class UserEnum(enum.Enum):
    ADMIN = 'Admin'
    READER = 'Reader'
    LIBRARIAN = 'Librarian'


class User(base.Base):
    __tablename__ = "User"
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
    user_type:Mapped[UserEnum] = mapped_column(default=UserEnum.READER)

