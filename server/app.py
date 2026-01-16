from flask import Flask, request
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return {"error": "Plant not found"}, 404

        return {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": plant.price,
            "is_in_stock": plant.is_in_stock
        }, 200

    def patch(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return {"error": "Plant not found"}, 404

        data = request.get_json()
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]

        db.session.commit()

        return {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": plant.price,
            "is_in_stock": plant.is_in_stock
        }, 200

    def delete(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()

        return {}, 204


api.add_resource(PlantByID, '/plants/<int:id>')


with app.app_context():
    db.create_all()

    # required seed for tests
    if not Plant.query.first():
        plant = Plant(
            name="Aloe",
            image="https://example.com/aloe.jpg",
            price=11.50,
            is_in_stock=True
        )
        db.session.add(plant)
        db.session.commit()
