import pytest
from src.app.main import create_app, db, Client, Parking, ClientParking
from datetime import datetime, timedelta


@pytest.fixture
def app():
    app = create_app()

    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_data(app):
    client_obj = Client(
        name='John',
        surname='Doe',
        credit_card='1234-5678-9012-3456',
        car_number='ABC123'
    )
    db.session.add(client_obj)

    parking_obj = Parking(
        address='123 Main St',
        opened=True,
        count_places=10,
        count_available_places=10
    )
    db.session.add(parking_obj)
    db.session.commit()

    log_in = ClientParking(
        client_id=client_obj.id,
        parking_id=parking_obj.id,
        time_in=datetime.now() - timedelta(hours=2))
    parking_obj.count_available_places -= 1
    db.session.add(log_in)
    db.session.commit()

    return {
        'client': client_obj,
        'parking': parking_obj,
        'log_in': log_in,
    }
