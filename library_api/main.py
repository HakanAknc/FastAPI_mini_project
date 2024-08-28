from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modeller 
class Book(BaseModel):
    id: int
    title: str
    author_id: int
    year: int

class Author(BaseModel):
    id: int
    name: str
    nationality: str

# Geçici veri depoları
books  = []
authors  = []

# Kitap endpoints
@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.post("/books", response_model=Book)
def create_book(book: Book):
    for existing_book in books:
        if existing_book.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return {"message" : "Book  deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# Yazar Endpoints
@app.get("/authors", response_model=List[Author])
def get_authors():
    return authors

@app.post("/authors", response_model=Author)
def create_author(author: Author):
    for existing_author in authors:
        if existing_author.id == author.id:
            raise HTTPException(status_code=400, detail="Author with this ID already exists")
    authors.append(author)
    return author

@app.put("/authors/{author_id}", response_model=Author)
def update_author(author_id: int, updated_author: Author):
    for index, author in enumerate(authors):
        if author.id == author_id:
            authors[index] = updated_author
            return updated_author
    raise HTTPException(status_code=404, detail="Author not found")

@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    for index, author in enumerate(authors):
        if author.id == author_id:
            authors.pop(index)
            return {"message": "Author deleted successfully"}
    raise HTTPException(status_code=404, detail="Author not found")