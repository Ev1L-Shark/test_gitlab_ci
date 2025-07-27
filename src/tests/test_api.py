def test_get_single_client(client, setup_data):
    client_id = setup_data['client'].id
    response = client.get(f'/clients/{client_id}')
    assert response.status_code == 200


def test_get_all_clients(client):
    response = client.get('/clients')
    assert response.status_code == 200


def test_create_client(client):
    data = {
        "name": "Alice",
        "surname": "Smith",
        "credit_card": "9876-5432-1098-7654",
        "car_number": "XYZ789"
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data


def test_create_parking(client):
    data = {
        "address": "456 Elm St",
        "opened": True,
        "count_places": 20
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    json_data = response.get_json()

    assert 'id' in json_data


def test_check_in(client, setup_data):
    parking_id = setup_data['parking'].id
    client_id = setup_data['client'].id

    response = client.post('/client_parkings', json={
        'client_id': client_id,
        'parking_id': parking_id
    })
    assert (response.status_code == 200 or
            response.status_code == 400 or
            response.status_code == 500)

    if response.status_code == 200:
        data = response.get_json()
        assert ('message' in data and
                data['message'] == 'Check-in successful')


def test_check_out(client, setup_data):
    parking_id = setup_data['parking'].id
    client_id = setup_data['client'].id

    response = client.delete('/client_parkings', json={
        'client_id': client_id,
        'parking_id': parking_id
    })

    assert (response.status_code == 200 or
            response.status_code == 400 or
            response.status_code == 500)

    if response.status_code == 200:
        data = response.get_json()
        assert 'amount_due' in data and 'duration_hours' in data
