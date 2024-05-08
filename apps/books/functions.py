from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from apps.books import crud, schema, filters
from apps.users import crud as user_crud, models as user_model
from book_management.core.permission import role_permissions
from book_management.core.constant import UserEnum


def get_all_books(db, user_id):
    books = crud.get_books(db)
    user = user_crud.get_user_by_userid(db, user_id)

    if user.user_type == user_model.UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(books))

    return jsonable_encoder(books)


def get_a_book(db, user_id, book_id):
    user = user_crud.get_user_by_userid(db, user_id)
    book = crud.get_a_books(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "item not found"}
        )

    if user.user_type == user_model.UserEnum.READER:
        adapter = TypeAdapter(schema.BooksSchema)
        return jsonable_encoder(adapter.dump_python(book))

    return jsonable_encoder(book)


@role_permissions(roles=[UserEnum.LIBRARIAN])
def create_book_item(db, user_id, book):
    user = user_crud.get_user_by_userid(db, user_id)

    if crud.create_book_item(db, user, book):
        return {"message": "book added succesfully"}


@role_permissions(roles=[UserEnum.LIBRARIAN])
def edit_book_item(db, user_id, book_id, book):
    user = user_crud.get_user_by_userid(db, user_id)

    if crud.update_book(db, user, book, book_id):
        return {"message": "updatation succesfully"}

    raise HTTPException(
        status_code=404,
        detail={"error": "Item not found"}
    )

@role_permissions(roles=[UserEnum.LIBRARIAN])
def delete_book_item(db, user_id, book_id):
    if crud.remove_book_item(db, book_id):
        return {"message": "item deleted succesfully"}

    raise HTTPException(
        status_code=400,
        detail={"error": "item not found"}
    )

@role_permissions(roles=[UserEnum.LIBRARIAN])
def borrow_book(db, user_id, book_id):
    users_obj = user_crud.get_a_reader(db, user_id)
    book_obj = crud.get_a_books(db, book_id)

    if book_obj is None or book_obj.is_available == False:
        raise HTTPException(
            status_code=400, detail={
                "error": "This book not available"}
        )

    if crud.borrow_book(db, users_obj, book_obj):
        return {"message": "book transaction is started"}

    raise HTTPException(
        status_code=400,
        detail={"error": " your transaction didn't ended please contact admin"}
    )


def return_book(db: Session, user_id, book_id):
    users_obj = user_crud.get_a_reader(db, user_id)
    book_obj = crud.get_a_books(db, book_id)

    if crud.return_book(db, users_obj, book_obj):
        return {"message": "Book transaction updated and ended"}

    raise HTTPException(
        status_code=400,
        detail={"error": "transaction not found"}
    )


def return_book_history(db: Session, user_int: int):
    history = crud.return_book_history(db, user_int)
    adapter = TypeAdapter(list[schema.BookTransactionSchema])
    result = adapter.dump_python(history)

    if not result:
        return {"error": "empty results"}
    return jsonable_encoder(result)


def search_book(db: Session, user_id: int, search : filters.FilterModelBook):
    results = crud.search_book(db, search)
    user = user_crud.get_user_by_userid(db, user_id)

    if not results:
        return {"message": "could not found"}

    if user.user_type == user_model.UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(results))

    return jsonable_encoder(results)
