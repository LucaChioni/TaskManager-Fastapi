from fastapi import APIRouter, HTTPException
from models.task import Task, NewTask, UpdatedTask

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

tasks = [
    Task(id=1, title="Task 1", completed=False),
    Task(id=2, title="Task 2", completed=True),
    Task(id=3, title="Task 3", completed=False),
]

@router.get("")
async def get_tasks() -> list[Task]:
    return tasks

@router.get("/{task_id}")
async def get_task(task_id: int) -> Task:
    task = next((task for task in tasks if task.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.post("")
async def create_tasks(new_tasks: list[NewTask]) -> list[Task]:
    created_tasks = []
    for new_task in new_tasks:
        new_id = max(task.id for task in tasks) + 1 if tasks else 1
        task = Task(id=new_id, **new_task.model_dump())
        created_tasks.append(task)

    tasks.extend(created_tasks)
    return created_tasks

@router.put("/{task_id}")
async def update_task(updated_task: UpdatedTask) -> Task:
    task = next((task for task in tasks if task.id == updated_task.id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.update(updated_task.model_dump(exclude_unset=True))
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: int) -> bool:
    task = next((task for task in tasks if task.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(task)
    return True
