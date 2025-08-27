from flask import jsonify
from models.enums import ClientStatusEnum

def check_client_verification_route(Client, FamilyAndToiletStatus):
    def check_client_verification(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Get status message based on the client's current status
            status_messages = {
                ClientStatusEnum.PENDING: 'Client is pending verification',
                ClientStatusEnum.VERIFIED: 'Client is verified',
                ClientStatusEnum.REJECTED: 'Client has been rejected'
            }
            
            return jsonify({
                'client_id': client_id,
                'status': client.status.value,
                'verified': client.verified,  
                'is_rejected': client.status == ClientStatusEnum.REJECTED,
                'message': status_messages.get(client.status, 'Unknown status')
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return check_client_verification
