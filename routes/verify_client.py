from flask import jsonify
from models.enums import ClientStatusEnum

def verify_client_route(db, Client):
    def verify_client(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Check if client is already verified
            if client.status == ClientStatusEnum.VERIFIED:
                return jsonify({'error': 'Client is already verified'}), 400
            
            # Check if client is rejected
            if client.status == ClientStatusEnum.REJECTED:
                return jsonify({'error': 'Cannot verify a rejected client'}), 400
            
            # Set status to VERIFIED
            client.status = ClientStatusEnum.VERIFIED
            client.verified = True  # Keep verified field in sync for backward compatibility
            db.session.commit()
            
            return jsonify({
                'client_id': client_id,
                'status': client.status.value,
                'verified': True,
                'message': 'Client has been successfully verified'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return verify_client
