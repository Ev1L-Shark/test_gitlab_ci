import pytest
from src.tests.factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(client):
    new_client = ClientFactory()

    response = client.post('/clients', json={
        "name": new_client.name,
        "surname": new_client.surname,
        "credit_card": new_client.credit_card,
        "car_number": new_client.car_number,
    })

    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data


def test_create_parking_with_factory(client):
    new_parking = ParkingFactory()

    response = client.post('/parkings', json={
        "address": new_parking.address,
        "opened": new_parking.opened,
        "count_places": new_parking.count_places,
    })

    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data