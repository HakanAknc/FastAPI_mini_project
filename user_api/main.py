from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Veri modeliniz
class User(BaseModel):
    name: str
    age: int
    email: str

# Veri tabanı simülasyonu
fake_db = {}

# Create (Oluşturma) - Post isteği
@app.post("/users")
def create_user(user: User):
    user_id = len(fake_db) + 1
    fake_db[user_id] = user
    return {"user_id": user_id, "user": user}

# Read (Okuma) - GET isteği
@app.get("/user/{user_id}")
def read_user(user_id: int):
    user = fake_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "user": user}

# Update (Güncelleme) - Put isteği
@app.put("/user/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    
# Delete (Silme) - Delete isteği
@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return {"message": "User deleted seccessfully"}