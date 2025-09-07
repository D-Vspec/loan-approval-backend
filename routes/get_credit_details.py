# filepath: routes/get_credit_details.py
from flask import jsonify

def get_credit_details_route(Client, CreditAssessmentSummary):
    def get_credit_details(client_id):
        try:
            # Ensure client exists
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

            # Fetch the client's credit assessment summary (single row per client)
            credit = CreditAssessmentSummary.query.filter_by(client_id=client_id).first()
            if not credit:
                return jsonify({'error': 'Credit details not found'}), 404

            def to_float(d):
                return float(d) if d is not None else None

            return jsonify({
                'client_id': client_id,
                'credit': {
                    'id': credit.id,
                    'capacityScore': to_float(credit.capacity_score),
                    'capacityCreditScore': to_float(credit.capacity_credit_score),
                    'residencyScore': to_float(credit.residency_score),
                    'residencyCreditScore': to_float(credit.residency_credit_score),
                    'recordScore': to_float(credit.record_score),
                    'recordCreditScore': to_float(credit.record_credit_score),
                    'centerScore': to_float(credit.center_score),
                    'centerCreditScore': to_float(credit.center_credit_score),
                    'creditScore': to_float(credit.credit_score),
                    'riskGrade': credit.risk_grade,
                    'createdAt': credit.created_at.isoformat() if credit.created_at else None,
                }
            }), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    return get_credit_details
