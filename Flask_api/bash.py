from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from faker import Faker

app = Flask(__name__)
api = Api(app)
fake = Faker()

# Rastgele 10 kişi oluştur
people = [
    {'id': i + 1, 'first_name': fake.first_name(), 'last_name': fake.last_name(),
     'phone': fake.phone_number(), 'email': fake.email()}
    for i in range(10)
]

# Kişi listesini yönetmek için endpoint
class PersonList(Resource):
    def get(self):
        return people, 200

    def post(self):
        new_person = request.get_json()
        new_person['id'] = len(people) + 1
        people.append(new_person)
        return new_person, 201

# Tek bir kişiyi almak, güncellemek ve silmek için endpoint
class Person(Resource):
    def get(self, person_id):
        person = next((p for p in people if p['id'] == person_id), None)
        if person:
            return person, 200
        return {'message': 'Person not found'}, 404

    def put(self, person_id):
        person = next((p for p in people if p['id'] == person_id), None)
        if person:
            data = request.get_json()
            person.update(data)
            return person, 200
        return {'message': 'Person not found'}, 404

    def delete(self, person_id):
        global people
        people = [p for p in people if p['id'] != person_id]
        return '', 204

# Endpointleri API'ye ekleyin
api.add_resource(PersonList, '/people')
api.add_resource(Person, '/people/<int:person_id>')

if __name__ == '__main__':
    app.run(debug=True)
