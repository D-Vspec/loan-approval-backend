from flask import jsonify

def verify_client_route(db, Client):
    def verify_client(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Check if client is already verified
            if client.verified:
                return jsonify({'error': 'Client is already verified'}), 400
            
            # Set verified to True
            client.verified = True
            db.session.commit()
            
            return jsonify({
                'client_id': client_id,
                'verified': True,
                'message': 'Client has been successfully verified'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return verify_client
