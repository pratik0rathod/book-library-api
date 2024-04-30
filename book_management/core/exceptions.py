from apps.users import crud,constant

from traceback import print_exception
from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# regular user exception decorator
def reguler_user_exception(func):
  def wrapper(*args,**kwargs):
    user = crud.get_user_by_userid(args[0],args[1])
    
    if user.user_type == constant.UserEnum.READER:
        raise HTTPException(status_code=401,detail={"error":"You are not allowed to perform this action"})
    
    result = func(*args,**kwargs)
    return result
  return wrapper

#gobal Exceptionhandler middleware
class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
      
        except HTTPException as http_exception:
            print_exception(http_exception)
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
            
        except Exception as e:
            print_exception(e) 
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )