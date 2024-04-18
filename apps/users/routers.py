from fastapi import APIRouter

user_router  = APIRouter(prefix='/user',tags=['User'])

@user_router.get("/")
async def get():
    return {"message":"please wait under developement"}

@user_router.post("/register")
async def register_user():
    return {"message":"please wait under developement"}

@user_router.post("/login")
async def login_user():
    return {"message":"please wait under developement"}

@user_router.get("/me")
async def get_me():
    return {"message":"please wait under developement"}
