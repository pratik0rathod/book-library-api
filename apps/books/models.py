from . import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship,backref

from datetime import datetime


class Book(base.Base):
    title:Mapped[str]
    author:Mapped[str]
    publication_date:Mapped[datetime] 
    ratings:Mapped[float]
    
    added_by_id:Mapped[int] = mapped_column(ForeignKey("user.id"),nullable=True)
    
    user:Mapped["User"] =  relationship(backref=="user")

from apps.users.models import User
