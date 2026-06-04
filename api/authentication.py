from fastapi import APIRouter, HTTPException
from models.authentication import Credentials

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/login")
async def login(credentials: Credentials) -> dict:
    if credentials.username == "admin" and credentials.password == "password":
        return {"token": "fake-jwt-token"}

    raise HTTPException(status_code=401, detail="Invalid username or password")

# @router.post("/register")
# async def register(credentials: Credentials) -> dict:
#     return {"message": "Registration successful", "username": credentials.username}
