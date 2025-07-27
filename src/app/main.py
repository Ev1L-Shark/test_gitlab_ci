from datetime import datetime

from flask import Flask, jsonify, request

from src.app.models import Client, ClientParking, Parking

from . import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        result = [client.to_json() for client in clients]
        return jsonify(result), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.filter(Client.id == client_id).first()
        result = client.to_json()
        return jsonify(result), 200

    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        credit_card = data.get('credit_card')
        car_number = data.get('car_number')

        new_client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'message': 'Client created', 'id': new_client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.get_json()
        address = data.get('address')
        opened = data.get('opened', True)
        count_places = data.get('count_places')
        count_available_places = count_places

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places
        )
        db.session.add(new_parking)
        db.session.commit()
        return jsonify({'message': 'Parking created',
                        'id': new_parking.id}), 201

    @app.route('/client_parkings', methods=['POST'])
    def check_in():
        data = request.get_json()
        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        client = Client.query.get_or_404(client_id)
        parking_obj = Parking.query.get_or_404(parking_id)

        if not parking_obj.opened:
            return jsonify({'error': 'Parking is closed'}), 400
        elif parking_obj.count_available_places <= 0:
            return jsonify({'error': 'No available places'}), 400

        new_log_in = ClientParking(
            client_id=client.id,
            parking_id=parking_obj.id,
            time_in=datetime.now()
        )

        parking_obj.count_available_places -= 1

        try:
            db.session.add(new_log_in)
            db.session.commit()
            return jsonify({'message': 'Check-in successful'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/client_parkings', methods=['DELETE'])
    def check_out():
        data = request.get_json()
        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        log_entry = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id).filter(
            ClientParking.time_out is None).first()

        if not log_entry:
            return jsonify({'error': 'No active parking session found'}), 400

        client = db.session.query(Client).get(client_id)

        if not client or not client.credit_card:
            return jsonify({'error': 'Client has no credit card linked'}), 400

        parking_obj = db.session.query(Parking).get(parking_id)

        log_entry.time_out = datetime.now()

        duration_seconds = int(
            (log_entry.time_out - log_entry.time_in).total_seconds())
        duration_hours = duration_seconds / 3600

        rate_per_hour = 2.0
        amount_due = round(duration_hours * rate_per_hour, 2)

        payment_successful = True

        if payment_successful:
            parking_obj.count_available_places += 1
            db.session.commit()
            return jsonify({
                'message': 'Check-out successful',
                'amount_due': amount_due,
                'duration_hours': duration_hours
            }), 200
        else:
            raise Exception("Payment failed")

    return app
