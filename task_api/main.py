from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Görev veri modeli
class Task(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool = False

# Başlangıçta boş bir görev listesi
tasks: List[Task] = []

# Tüm görevleri listeleme
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Yeni bir görev ekleme
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    # Aynı ID'ye sahip bir görev varsa hata ver
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# Görev güncelleme
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    for index, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            tasks[index] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Görev silme
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            del tasks[index]
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
