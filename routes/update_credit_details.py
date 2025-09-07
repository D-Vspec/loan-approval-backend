# filepath: routes/update_credit_details.py
from flask import request, jsonify
from routes.utils import parse_decimal


def update_credit_details_route(db, Client, CreditAssessmentSummary):
    def update_credit_details(client_id):
        try:
            # Validate client exists
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

            payload = request.get_json(silent=True) or {}

            # Find or create the credit summary row for this client
            credit = CreditAssessmentSummary.query.filter_by(client_id=client_id).first()
            if not credit:
                credit = CreditAssessmentSummary(client_id=client_id)
                db.session.add(credit)
                # flush so credit gets an id if needed later
                db.session.flush()

            # Map incoming camelCase keys to model attributes
            mapping = {
                'capacityScore': 'capacity_score',
                'capacityCreditScore': 'capacity_credit_score',
                'residencyScore': 'residency_score',
                'residencyCreditScore': 'residency_credit_score',
                'recordScore': 'record_score',
                'recordCreditScore': 'record_credit_score',
                'centerScore': 'center_score',
                'centerCreditScore': 'center_credit_score',
                'creditScore': 'credit_score',
                'riskGrade': 'risk_grade',
            }

            # Only update provided fields; allow explicit null to clear
            for incoming_key, model_attr in mapping.items():
                if incoming_key in payload:
                    value = payload[incoming_key]
                    if model_attr == 'risk_grade':
                        setattr(credit, model_attr, value if value not in ("", None) else None)
                    else:
                        # numeric/decimal fields
                        if value in (None, ""):
                            setattr(credit, model_attr, None)
                        else:
                            setattr(credit, model_attr, parse_decimal(value))

            db.session.commit()

            # Build response
            def to_float(d):
                return float(d) if d is not None else None

            return jsonify({
                'message': 'Credit details updated successfully',
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
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    return update_credit_details
