from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modeller
class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: str

class Teacher(BaseModel):
    id: int
    name: str
    subject: str

# Geçici veri depoları
students = []
teachers = []

# Öğrenci Endpoints
@app.get("/students",response_model=List[Student])
def get_students():
    return students

@app.post("/students", response_model=Student)
def create_student(student: Student):
    for existing_student in students:
        if existing_student.id == student.id:
            raise HTTPException(status_code=400, detail="Bu kimliğe sahip öğrenci zaten mevcut")
    students.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = update_student
            return updated_student
    raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            students.pop(index)
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")


# Öğretmen Endpoints
@app.get("/teachers", response_model=List[Teacher])
def get_teachers():
    return teachers

@app.post("/teachers", response_model=List[Teacher])
def create_teacher(teacher: Teacher):
    for existing_teacher in teachers:
        if existing_teacher.id == teacher.id:
            raise HTTPException(status_code=400, detail="Bu kimliğe sahip öğretmen zaten mevcut.")
    teachers.append(teacher)
    return teacher

@app.put("/teachers/{teacher_id}", response_model=List[Teacher])
def update_teacher(teacher_id: int, updated_teacher: Teacher):
    for index, teacher in enumerate(teachers):
        if teacher.id == teacher_id:
            teachers[index] = update_teacher
            return update_teacher
    raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    for index, teacher in enumerate(teachers):
        if teacher.id == teacher_id:
            teachers.pop(index)
            return {"message": "Öğretmen başarıyla silindi."}
        raise HTTPException(status_code=404, detail="Öğretmen başarıyla silindi")
