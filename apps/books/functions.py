from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from apps.books import schema, filters, models
from apps.books.crud import book_action, book_transaction_action
from apps.users.models import Users
from book_management.core.constant import UserEnum
from book_management.core.permission import role_permissions


@role_permissions(roles=[UserEnum.LIBRARIAN])
def count_books(db: Session, user: Users):
    return book_action.count(db)


@role_permissions(roles=[UserEnum.LIBRARIAN])
def get_all_books(db: Session, user: Users):
    books = book_action.get_multi(db, filters=False, sorting=False)

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(books))

    return jsonable_encoder(books)


@role_permissions(roles=[UserEnum.LIBRARIAN])
def get_a_book(db: Session, user: Users, book_id: int):
    book = book_action.get(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "item not found"}
        )

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(schema.BooksSchema)
        return jsonable_encoder(adapter.dump_python(book))

    return jsonable_encoder(book)


@role_permissions(roles=[UserEnum.LIBRARIAN])
def create_book_item(db: Session, user: Users, book: schema.BooksSchema):
    book = schema.AddBookSchema(
        **book.model_dump(),
        added_by=user.id
    )

    book_in = book_action.create(db, obj_in=book.model_dump())
    return book_in


@role_permissions(roles=[UserEnum.LIBRARIAN])
def edit_book_item(
        db: Session,
        user: Users,
        book_id: int,
        book: schema.BooksSchema
):
    book_obj = book_action.get(db, book_id)
    book_in = book_action.update(db, db_obj=book_obj, obj_in=book)
    return book_in


@role_permissions(roles=[UserEnum.LIBRARIAN])
def delete_book_item(db: Session, user: Users, book_id):
    if book_action.hard_delete(db, id=book_id):
        return {"message": f"item {book_id} deleted succesfully"}


def search_book(
        db: Session,
        user: Users,
        search: filters.FilterModelBook
):
    results = book_action.get_multi(db, filter_data=search, sorting=False)

    if not results:
        return {"message": "could not found"}

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(results))

    return jsonable_encoder(results)


def _get_book_transaction_obj(db: Session, book_obj: models.Books, user: Users):
    return book_transaction_action.filter_by(
        db,
        book_id=book_obj.id,
        user_id=user.id,
        return_date=None,
        raise_exc=False
    )


def borrow_book(db: Session, user: Users, book_id):
    book_obj = book_action.get(db, book_id)
    book_transaction_obj = _get_book_transaction_obj(
        db,
        book_obj=book_obj,
        user=user
    )

    if book_transaction_obj is None:
        if book_obj.is_available:
            book_action.update(
                db,
                db_obj=book_obj,
                obj_in={
                    'is_available': False,
                },
                autocommit=False
            )

            book_transaction_in = book_transaction_action.create(
                db,
                obj_in={
                    'user_id': user.id,
                    'book_id': book_obj.id
                },
                autocommit=False
            )
            db.commit()
            return book_transaction_in

        raise HTTPException(
            status_code=400,
            detail={
                "error": "This book not available"
            }
        )

    raise HTTPException(
        status_code=400,
        detail={"error": " your transaction didn't ended please contact admin"}
    )


def return_book(db: Session, user: Users, book_id):
    book_obj = book_action.get(db, book_id)
    book_transaction_obj = _get_book_transaction_obj(
        db,
        book_obj=book_obj,
        user=user
    )

    if book_transaction_obj is not None:
        book_transaction_in = book_transaction_action.update(
            db,
            db_obj=book_transaction_obj,
            obj_in={
                "return_date": date.today()
            },
            autocommit=False
        )

        book_action.update(
            db,
            db_obj=book_obj,
            obj_in={
                'is_available': True,
            },
            autocommit=False
        )

        db.commit()

        return book_transaction_in

    raise HTTPException(
        status_code=400,
        detail={"error": "transaction not found"}
    )


def return_book_history(db: Session, user: Users):
    history = book_transaction_action.get_multi(
        db,
        filters=False,
        sorting=False,
        user_id=user.id,
        joined_load=models.BookTransaction.book
    )

    adapter = TypeAdapter(list[schema.BookTransactionSchema])
    history = adapter.dump_python(history)

    return jsonable_encoder(history)
