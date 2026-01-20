from fastapi import APIRouter

search_router = APIRouter()

@search_router.get("/ping")
def search_health():
    return {"message": "Search service placeholder"}