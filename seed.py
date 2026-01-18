from app import app
from models import db, Plant

with app.app_context():

    Plant.query.delete()

    plants = [
        Plant(
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50,
            is_in_stock=True
        ),
        Plant(
            name="ZZ Plant",
            image="./images/zz-plant.jpg",
            price=25.98,
            is_in_stock=True
        )
    ]

    db.session.add_all(plants)
    db.session.commit()

    print("Database seeded!")
