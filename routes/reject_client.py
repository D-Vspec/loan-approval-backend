from flask import jsonify, request
from models.enums import ClientStatusEnum

def reject_client_route(db, Client):
    def reject_client(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Check if client is already rejected
            if client.status == ClientStatusEnum.REJECTED:
                return jsonify({'error': 'Client is already rejected'}), 400
            
            # Check if client is already verified - optionally prevent rejection of verified clients
            if client.status == ClientStatusEnum.VERIFIED:
                return jsonify({'error': 'Cannot reject a verified client'}), 400
            
            # Get optional rejection reason from request body
            data = request.get_json() or {}
            rejection_reason = data.get('reason', '')
            
            # Set status to REJECTED
            client.status = ClientStatusEnum.REJECTED
            client.verified = False  # Keep verified field in sync for backward compatibility
            db.session.commit()
            
            response_data = {
                'client_id': client_id,
                'status': client.status.value,
                'verified': False,
                'message': 'Client has been successfully rejected'
            }
            
            if rejection_reason:
                response_data['reason'] = rejection_reason
            
            return jsonify(response_data), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return reject_client
