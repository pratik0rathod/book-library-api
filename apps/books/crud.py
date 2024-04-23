from sqlalchemy.orm import Session
from apps.books import models, schema
from apps.users.models import Users

from sqlalchemy import update


def get_books(db: Session):
    return db.query(models.Books).all()


def get_a_books(db: Session, book_id):
    return db.query(models.Books).filter(models.Books.id == book_id).first()


def create_book_item(db: Session, user: Users, book: schema.BooksSchema):

    book_obj = models.Books(**book.model_dump(),added_by=user.id,)
    print(book_obj.genre)
    db.add(book_obj)
    db.commit()
    return True


def remove_book_item(db: Session, book_id: int):
    item = db.query(models.Books).filter(models.Books.id == book_id).first()

    if item is not None:
        db.delete(item)
        db.commit()
        return True

    return False


def update_book(db: Session, user: Users, book: schema.BooksSchema, book_id: int):
    
    udq = update(models.Books).where(models.Books.id ==
                                     book_id).values(**book.model_dump())
    result = db.execute(udq)
    
    if result.rowcount == 1:
        db.commit()
        return True

    return False
    
    