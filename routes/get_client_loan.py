from flask import jsonify
from models.enums import ClientStatusEnum


def get_client_loan_route(Client, Loan):
    def get_client_loan(client_id):
        try:
            # Check if client exists
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Check if client is verified (has approved loans)
            if client.status != ClientStatusEnum.VERIFIED:
                return jsonify({
                    'error': 'Client is not verified',
                    'status': client.status.value,
                    'message': 'Only verified clients have approved loans'
                }), 400
            
            # Get the loan for this client
            loan = Loan.query.filter_by(client_id=client_id).first()
            
            if not loan:
                return jsonify({
                    'error': 'No approved loan found for this client',
                    'client_id': client_id,
                    'status': client.status.value,
                    'message': 'Client is verified but no loan record exists'
                }), 404
            
            # Return loan information
            return jsonify({
                'client_id': client_id,
                'loan_id': loan.loan_id,
                'interest_rate': float(loan.interest_rate) if loan.interest_rate else None,
                'payment_term': loan.payment_term,
                'client_status': client.status.value,
                'message': 'Loan found successfully'
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    return get_client_loan
