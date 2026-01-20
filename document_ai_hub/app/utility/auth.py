from fastapi import APIRouter

auth_router = APIRouter()    
@auth_router.get("/login")
async def login():
    return {"access_token": "dummy_token", "token_type": "bearer"}