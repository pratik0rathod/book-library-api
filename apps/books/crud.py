from sqlalchemy.orm import Session
from apps.books import models, schema
from apps.users.models import Users

from sqlalchemy import update

import datetime


def get_books(db: Session):
    return db.query(models.Books).all()


def get_a_books(db: Session, book_id):
    return db.query(models.Books).filter(models.Books.id == book_id).first()


def create_book_item(db: Session, user: Users, book: schema.BooksSchema):

    book_obj = models.Books(**book.model_dump(), added_by=user.id,)
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


def borrow_book(db: Session, user: models.Users, book: models.Books):
    # db.begin()
    book_transaction = db.query(models.BookTransaction).filter(
        models.BookTransaction.book_id == book.id, 
        models.BookTransaction.user_id == user.id,
        models.BookTransaction.return_date.is_(None),
        ).first()
    
    if book_transaction is not None:
        return False
    
    book_transaction = models.BookTransaction(user_id=user.id, book_id=book.id)
    book.is_available = False
    
    db.add(book)
    db.add(book_transaction)
    db.commit()
    return True

def return_book(db: Session, user: models.Users, book: models.Books):
    book.is_available = True

    book_transaction = db.query(models.BookTransaction).filter(
        models.BookTransaction.book_id == book.id, 
        models.BookTransaction.user_id == user.id,
        models.BookTransaction.return_date.is_(None),
        ).first()

    if book_transaction:
        # db.begin()

        book_transaction.return_date = datetime.date.today()
        book.is_available = True
        db.add(book_transaction)
        db.add(book)
        db.commit()
        return True
    return False
