from pydantic import TypeAdapter

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from apps.users import crud as usercrud,models as usermodel
from apps.books import crud,schema
from sqlalchemy.orm import Session
def get_all_books(db,user_id):

    try:
        books = crud.get_books(db)
        user = usercrud.get_user_by_userid(db,user_id)
        
        if user.user_type == usermodel.UserEnum.READER:        
            adapter = TypeAdapter(list[schema.BooksSchema])    
            return jsonable_encoder(adapter.dump_python(books))
        
        return jsonable_encoder(books)
    
    except HTTPException as h:
        raise h
    
    except Exception as e: 
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})
    
def get_a_book(db,user_id,book_id):
    try:
        
        user = usercrud.get_user_by_userid(db,user_id)
        book = crud.get_a_books(db,book_id)

        if book is None:
            raise HTTPException(status_code=404,detail={"error":"item not found"})
        
        # if user reader just give relavent information 
        
        if user.user_type == usermodel.UserEnum.READER:        
            adapter = TypeAdapter(schema.BooksSchema)    
            return jsonable_encoder(adapter.dump_python(book))
        
        return jsonable_encoder(book)
        
    except HTTPException as h:
        raise h
    
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})
   

def create_book_item(db,user_id,book):
    
    try:
        user = usercrud.get_user_by_userid(db,user_id)
        
        if user.user_type != usermodel.UserEnum.LIBRARIAN:
            raise HTTPException(status_code=400,detail={"error":"You are not allowed to perform this action"})
        
        if crud.create_book_item(db,user,book):
            return {"message":"book added succesfully"}
    
    except HTTPException as h:
        raise h
    
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

    
    
def edit_book_item(db,user_id,book_id,book):
    try:
        user = usercrud.get_user_by_userid(db,user_id)
        
        if user.user_type != usermodel.UserEnum.LIBRARIAN:
            raise HTTPException(status_code=400,detail={"error":"You are not allowed to perform this action"})
       
        if crud.update_book(db,user,book,book_id):
            return {"message":"updatation succesfully"}
        
        raise HTTPException(status_code=404,detail={"error":"Item not found"})
        
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})


def delete_book_item(db,user_id,book_id):
    try:
        user = usercrud.get_user_by_userid(db,user_id)
        
        if user.user_type != usermodel.UserEnum.LIBRARIAN:
            raise HTTPException(status_code=400,detail={"error":"You are not allowed to perform this action"})
      
        if crud.remove_book_item(db,book_id):
            return {"message":"item deleted succesfully"}
        
        raise HTTPException(status_code=400,detail={"error":"item not found"})

    
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})
    
    
def borrow_book(db,user_id,book_id):
    try:
        
        users_obj =  usercrud.get_a_reader(db,user_id)
        book_obj = crud.get_a_books(db,book_id)
      
        if book_obj is None or book_obj.is_available == False:
            raise HTTPException(status_code=400,detail={"error":"This book not available"})
        
        if crud.borrow_book(db,users_obj,book_obj):
            return {"message":"book transacation is started"}
        
        raise HTTPException(status_code=400,detail={"error":"Something went wrong - looks like your transacation didnt ended please contact admin"})
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

def return_book(db:Session,user_id,book_id):
   
    try:
        users_obj =  usercrud.get_a_reader(db,user_id)
        book_obj = crud.get_a_books(db,book_id)

        if crud.return_book(db,users_obj,book_obj):
            return {"meesage":"Book transaction updated and ended"}
        
        raise HTTPException(status_code=400,detail={"error":"trasacation not found"})

    except HTTPException as h:
        raise h
        
    except Exception as e: 
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

def return_book_history(db:Session,user_int:int):
    history = crud.return_book_history(db,user_int)
    adapter = TypeAdapter(list[schema.BookTransactionSchema])  
    result = adapter.dump_python(history)
    
    return jsonable_encoder(result)
    
    
def search_book(db:Session,user_int:int,search:str):
    results = crud.search_book(db,search)
    return jsonable_encoder(results)

