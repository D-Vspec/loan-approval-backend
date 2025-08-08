from flask import jsonify

def check_client_verification_route(Client):
    def check_client_verification(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            return jsonify({
                'client_id': client_id,
                'verified': client.verified,
                'message': f'Client is {"verified" if client.verified else "not verified"}'
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return check_client_verification
