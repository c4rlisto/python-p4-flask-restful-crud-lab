from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# ---------------- ROUTES ---------------- #

@app.get("/plants")
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200


@app.get("/plants/<int:id>")
def get_plant_by_id(id):
    plant = Plant.query.get(id)

    if not plant:
        return {"error": "Plant not found"}, 404

    return jsonify(plant.to_dict()), 200


@app.patch("/plants/<int:id>")
def update_plant(id):
    plant = Plant.query.get(id)

    if not plant:
        return {"error": "Plant not found"}, 404

    data = request.get_json()

    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]

    if "price" in data:
        plant.price = data["price"]

    db.session.commit()

    return jsonify(plant.to_dict()), 200


@app.delete("/plants/<int:id>")
def delete_plant(id):
    plant = Plant.query.get(id)

    if not plant:
        return {"error": "Plant not found"}, 404

    db.session.delete(plant)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
