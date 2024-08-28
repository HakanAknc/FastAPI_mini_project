from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Kitap modeli
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

# Kitapları saklamak için geçici bir veri deposu (list)
books = []

# Kitapları listeleme
@app.get("/books", response_model=List[Book])
def get_books():
    return books

# Yeni kitap ekleme
@app.post("/books", response_model=Book)
def add_book(book: Book):
    # Aynı ID'ye sahip bir kitap olup olmadığını kontrol et
    for existing_book in books:
        if existing_book.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

# Kitap güncelleme
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Kitap silme
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
