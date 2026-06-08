from fastapi import FastAPI
from database import Base, engine
from api.tasks import router as tasks_router
from api.authentication import router as auth_router

from models.user import User
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(tasks_router)
app.include_router(auth_router)
