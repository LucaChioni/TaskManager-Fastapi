from fastapi import FastAPI
from api.tasks import router as tasks_router
from api.authentication import router as auth_router

app = FastAPI()
app.include_router(tasks_router)
app.include_router(auth_router)
