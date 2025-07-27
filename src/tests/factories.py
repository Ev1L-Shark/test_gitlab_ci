import factory
from faker import Faker

from src.app.main import Client, Parking, db

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Maybe(
        factory.Faker("boolean"),
        yes_declaration=fake.credit_card_number(),
        no_declaration=None,
    )
    car_number = factory.Faker("bothify", text="??###")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("random_element", elements=[True, False])
    count_places = factory.Faker("random_int", min=1, max=10)
    count_available_places = count_places
