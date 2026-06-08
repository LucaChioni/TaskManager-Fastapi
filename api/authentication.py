import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Header, HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from database import get_db
from models.authentication import Credentials, UserResponse
from models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()


@router.post("/register")
async def register(credentials: Credentials, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.username == credentials.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=credentials.username, hashed_password=password_hash.hash(credentials.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful"}

@router.post("/login")
async def login(credentials: Credentials, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.username == credentials.username).first()
    if user and password_hash.verify(credentials.password, user.hashed_password):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid username or password")

@router.get("/me")
async def get_current_user(db: Session = Depends(get_db), authorization: str = Header(..., alias="Authorization")) -> UserResponse:
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token")
        token = parts[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return UserResponse.model_validate(user)
