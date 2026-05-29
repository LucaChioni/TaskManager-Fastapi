from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=50)
    completed: bool = False

    @field_validator("title", check_fields=False)
    @classmethod
    def title_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Title can't be empty")
        return value

    def update(self, data: dict):
        for field, value in data.items():
            setattr(self, field, value)

class NewTask(Task):
    id: int | None = None

class UpdatedTask(Task):
    title: str | None = Field(default=None, min_length=3, max_length=50)
    completed: bool | None = None
