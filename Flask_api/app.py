from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Örnek veri
books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell'},
    {'id': 2, 'title': 'Brave New World', 'author': 'Aldous Huxley'},
    {'id': 3, 'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'},
    {'id': 4, 'title': 'Hakan Akinc', 'author': 'Yazilim'}
]

# Kitapları listelemek ve yeni kitap eklemek için endpoint
class BookList(Resource):
    def get(self):
        return books, 200

    def post(self):
        new_book = request.get_json()
        new_book['id'] = len(books) + 1
        books.append(new_book)
        return new_book, 201

# Tek bir kitabı almak, güncellemek ve silmek için endpoint
class Book(Resource):
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            return book, 200
        return {'message': 'Book not found'}, 404

    def put(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            data = request.get_json()
            book.update(data)
            return book, 200
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        global books
        books = [book for book in books if book['id'] != book_id]
        return '', 204

# Endpointleri API'ye ekleyin
api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
