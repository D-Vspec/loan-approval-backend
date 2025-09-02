from flask import jsonify, request
from models.enums import ClientStatusEnum


def verify_client_route(db, Client, Loan):
    def verify_client(client_id):
        try:
            # Get JSON data from request
            json_data = request.get_json()
            if not json_data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Extract interest rate and payment term
            interest_rate = json_data.get('interest_rate')
            payment_term = json_data.get('payment_term')
            
            # Validate required fields
            if interest_rate is None or payment_term is None:
                return jsonify({
                    'error': 'Interest rate and payment term are required'
                }), 400
            
            # Validate data types
            try:
                interest_rate = float(interest_rate)
                payment_term = int(payment_term)
            except (ValueError, TypeError):
                return jsonify({
                    'error': 'Interest rate must be a number and payment term must be an integer'
                }), 400
            
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Check if client is already verified
            
            print(client.status)

            if client.status == ClientStatusEnum.VERIFIED:
                return jsonify({'error': 'Client is already verified'}), 400
            
            # Check if client is rejected
            if client.status == ClientStatusEnum.REJECTED:
                return jsonify({'error': 'Cannot verify a rejected client'}), 400
            
            # Set status to VERIFIED
            client.status = ClientStatusEnum.VERIFIED
            client.verified = True  # Keep verified field in sync for backward compatibility

            loan = Loan()
            loan.client_id = client_id
            loan.interest_rate = interest_rate
            loan.payment_term = payment_term
            db.session.add(loan)

            db.session.commit()
            
            return jsonify({
                'client_id': client_id,
                'status': client.status.value,
                'verified': True,
                'interest_rate': float(loan.interest_rate),
                'payment_term': loan.payment_term,
                'loan_id': loan.loan_id,
                'message': 'Client has been successfully approved with loan terms'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return verify_client
