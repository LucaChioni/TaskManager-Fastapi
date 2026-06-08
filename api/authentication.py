from fastapi import APIRouter, Header, HTTPException
from models.authentication import Credentials, User
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import os


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = [
    User(id=1, username="admin", hashed_password=pwd_context.hash("password")),
    User(id=2, username="user1", hashed_password=pwd_context.hash("password1")),
]

@router.post("/register")
async def register(credentials: Credentials) -> dict:
    user = next((user for user in users if user.username == credentials.username), None)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_id = max(user.id for user in users) + 1 if users else 1
    users.append(User(id=new_id, username=credentials.username, hashed_password=pwd_context.hash(credentials.password)))
    return {"message": "Registration successful"}

@router.post("/login")
async def login(credentials: Credentials) -> dict:
    user = next((user for user in users if user.username == credentials.username), None)
    if user and pwd_context.verify(credentials.password, user.hashed_password):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")

@router.get("/me")
async def get_current_user(authorization: str = Header(..., alias="Authorization")) -> dict:
    try:
        # Check and remove "Bearer " prefix
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

    user = next((user for user in users if user.username == username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user.model_dump(exclude={"hashed_password"})
