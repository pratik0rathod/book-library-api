from . import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship,backref

from datetime import datetime

# Implement age rating for books/manga 

class Books(base.Base):
    __tablename__ = "books"
    
    title:Mapped[str]
    isbn:Mapped[str]
    author:Mapped[str]
    publication_date:Mapped[datetime] 
    ratings:Mapped[float]

    user = relationship("Users", back_populates="books")
    

from apps.users.models import Users
