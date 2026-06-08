from pydantic import BaseModel


class Credentials(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
