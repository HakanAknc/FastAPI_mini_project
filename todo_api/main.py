from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# FastAPI uygulmasını başlat
app = FastAPI()

# Görev modeli
class Todo(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

# Görevleri saklamak için geçici bir veri deposu (list)
todos = []

# Tüm görevleri listele
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

# Yeni görev ekleme
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

# Bir görevi güncelle
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Güncellenecek todo bulunmadı.")

# Bir görevi sil
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo başarıyla silindi."}
    raise HTTPException(status_code=404, detail="Silinecek todo bulunmadı")