from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
    {"id": 3, "title": "Task 3", "completed": False},
]

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.post("/tasks")
async def create_tasks(new_task: TaskCreate):
    task_dict = new_task.model_dump()
    task_dict["id"] = max(task["id"] for task in tasks) + 1 if tasks else 1
    tasks.append(task_dict)
    return task_dict

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: TaskUpdate):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.update(updated_task.model_dump(exclude_unset=True))
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(task)
    return True

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)
