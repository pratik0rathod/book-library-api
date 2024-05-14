from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio.session import AsyncSession

from apps.books import schema, filters, models
from apps.books.crud import book_action, book_transaction_action
from apps.users.models import Users
from book_management.core.constant import UserEnum


async def count_books(db: AsyncSession):
    return await book_action.count(db)


async def get_all_books(db: AsyncSession, user: Users):
    books = await book_action.get_multi(db, filters=False, sorting=False)

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(books))

    return jsonable_encoder(books)


async def get_a_book(db: AsyncSession, user: Users, book_id: int):
    book = await book_action.get(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "item not found"}
        )

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(schema.BooksSchema)
        return jsonable_encoder(adapter.dump_python(book))

    return jsonable_encoder(book)


async def create_book_item(db: AsyncSession, user: Users, book: schema.BooksSchema):
    book = schema.AddBookSchema(
        **book.model_dump(),
        added_by=user.id
    )

    book_in = await book_action.create(db, obj_in=book.model_dump())
    return book_in


async def edit_book_item(
        db: AsyncSession,
        book_id: int,
        book: schema.BooksSchema
):
    book_obj = await book_action.get(db, book_id)
    book_in = await book_action.update(db, db_obj=book_obj, obj_in=book)
    return book_in


async def delete_book_item(db: AsyncSession, book_id):
    if await book_action.hard_delete(db, id=book_id):
        return {"message": f"item {book_id} deleted successfully"}


async def search_book(
        db: AsyncSession,
        user: Users,
        search: filters.FilterModelBook
):
    results = await book_action.get_multi(db, filter_data=search, sorting=False)

    if not results:
        return {"message": "could not found"}

    if user.user_type == UserEnum.READER:
        adapter = TypeAdapter(list[schema.BooksSchema])
        return jsonable_encoder(adapter.dump_python(results))

    return jsonable_encoder(results)


async def borrow_book(db: AsyncSession, user: Users, book_id):
    book_obj = await book_action.get(db, book_id)

    book_transaction_obj = await book_transaction_action.filter_by(
        db,
        book_id=book_obj.id,
        user_id=user.id,
        return_date=None,
        raise_exc=False
    )

    if book_transaction_obj is None:
        if book_obj.is_available:
            await book_action.update(
                db,
                db_obj=book_obj,
                obj_in={
                    'is_available': False,
                },
                autocommit=False
            )

            book_transaction_in = await book_transaction_action.create(
                db,
                obj_in={
                    'user_id': user.id,
                    'book_id': book_obj.id
                },
                autocommit=False
            )
            await db.commit()
            return book_transaction_in

        raise HTTPException(
            status_code=400,
            detail={
                "error": "This book not available"
            }
        )

    raise HTTPException(
        status_code=400,
        detail={
            "error": "Your transaction didn't ended please contact admin"
        }
    )


async def return_book(db: AsyncSession, user: Users, book_id):
    book_obj = await book_action.get(db, book_id)

    book_transaction_obj = await book_transaction_action.filter_by(
        db,
        book_id=book_obj.id,
        user_id=user.id,
        return_date=None,
        raise_exc=False
    )

    if book_transaction_obj is not None:
        book_transaction_in = await book_transaction_action.update(
            db,
            db_obj=book_transaction_obj,
            obj_in={
                "return_date": date.today()
            },
            autocommit=False
        )

        await book_action.update(
            db,
            db_obj=book_obj,
            obj_in={
                'is_available': True,
            },
            autocommit=False
        )

        await db.commit()

        return book_transaction_in

    raise HTTPException(
        status_code=400,
        detail={"error": "transaction not found"}
    )


async def return_book_history(db: AsyncSession, user: Users):
    history = await book_transaction_action.get_multi(
        db,
        filters=False,
        sorting=False,
        user_id=user.id,
        joined_load=models.BookTransaction.book
    )
    
    return jsonable_encoder(history)
