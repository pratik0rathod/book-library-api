from . import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship,backref

from datetime import date

# Implement age rating for books/manga 

class Books(base.Base):
    __tablename__ = "books"
    
    title:Mapped[str]
    isbn:Mapped[str]
    author:Mapped[str]
    publication_date:Mapped[date] 
    ratings:Mapped[float]
    added_by:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=True)
    user = relationship("Users", back_populates="books")

from apps.users.models import Users
