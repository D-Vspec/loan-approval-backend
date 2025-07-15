from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

# Create blueprint
client_bp = Blueprint('client', __name__)

@client_bp.route('/process_form_data', methods=['POST'])
def process_form_data():
    try:
        # Import models and db inside the function to avoid circular imports
        from models import Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense
        from db import db
        
        # Get JSON data from request
        json_data = request.get_json()
        
        if not json_data or 'data' not in json_data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        data = json_data['data']
        
        # Create Client instance
        client = Client()
        
        # Map and set basic client information
        client.salutation = map_salutation(data.get('salutation', ''))
        client.last_name = data.get('lastName', '')
        client.first_name = data.get('firstName', '')
        client.middle_name = data.get('middleName', '')
        client.gender = map_gender(data.get('gender', ''))
        client.birthdate = parse_date(data.get('birthDate'))
        client.place_of_birth = data.get('placeOfBirth', '')
        client.height = parse_decimal(data.get('height'))
        client.contact_number = data.get('contactNumber', '')
        client.no_of_dependents = parse_int(data.get('numberOfDependents'))
        client.marital_status = map_marital_status(data.get('maritalStatus', ''))
        client.nationality = data.get('nationality', '')
        client.weight = parse_decimal(data.get('weight'))
        client.education = data.get('education', '')
        client.spouse_name = data.get('spouseName', '')
        client.spouse_birthdate = parse_date(data.get('spouseBirthDate'))
        client.work = data.get('spouseWork', '')
        client.monthly_income = parse_decimal(data.get('spouseMonthlyIncome'))
        
        # Add client to session
        db.session.add(client)
        db.session.flush()  # This assigns an ID to the client
        
        # Create Address Information
        address = AddressInformation()
        address.client_id = client.id
        address.street = data.get('streetAddress', '')
        address.barangay = data.get('barangay', '')
        address.city_municipality = data.get('cityMunicipality', '')
        address.province = data.get('province', '')
        address.region = data.get('region', '')
        db.session.add(address)
        
        # Create Beneficiaries
        beneficiaries_data = data.get('beneficiaries', [])
        for beneficiary_data in beneficiaries_data:
            beneficiary = Beneficiaries()
            beneficiary.client_id = client.id
            beneficiary.name = beneficiary_data.get('name', '')
            beneficiary.birthdate = parse_date(beneficiary_data.get('birthDate'))
            beneficiary.age = parse_int(beneficiary_data.get('age'))
            beneficiary.relationship = beneficiary_data.get('relationship', '')
            db.session.add(beneficiary)
        
        # Create Co-Insured
        co_insured_data = data.get('coInsured', [])
        for co_insured_item in co_insured_data:
            co_insured = CoInsured()
            co_insured.client_id = client.id
            co_insured.name = co_insured_item.get('name', '')
            co_insured.birthdate = parse_date(co_insured_item.get('birthDate'))
            co_insured.age = parse_int(co_insured_item.get('age'))
            co_insured.relationship = co_insured_item.get('relationship', '')
            db.session.add(co_insured)
        
        # Process income data (if present in future versions)
        # This can be extended based on your form structure
        
        # Process expense data (if present in future versions)
        # This can be extended based on your form structure
        
        # Commit all changes
        db.session.commit()
        
        return jsonify({
            'message': 'Client data processed successfully',
            'client_id': client.id,
            'submission_date': json_data.get('submissionDate'),
            'form_type': json_data.get('formType')
        }), 201
        
    except Exception as e:
        from db import db
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@client_bp.route('/client/<int:client_id>', methods=['GET'])
def get_client_details(client_id):
    try:
        # Import models inside the function to avoid circular imports
        from models import Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense
        
        # Fetch client with all related data
        client = Client.query.get(client_id)
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Get related data
        address = AddressInformation.query.filter_by(client_id=client_id).first()
        beneficiaries = Beneficiaries.query.filter_by(client_id=client_id).all()
        co_insured = CoInsured.query.filter_by(client_id=client_id).all()
        incomes = Income.query.filter_by(client_id=client_id).all()
        expenses = Expense.query.filter_by(client_id=client_id).all()
        
        # Build response in the same format as input
        response_data = {
            "submissionDate": datetime.now().isoformat() + "Z",
            "formType": "Client Information Sheet",
            "data": {
                "salutation": reverse_map_salutation(client.salutation),
                "lastName": client.last_name or "",
                "firstName": client.first_name or "",
                "middleName": client.middle_name or "",
                "gender": reverse_map_gender(client.gender),
                "birthDate": format_date_to_iso(client.birthdate),
                "placeOfBirth": client.place_of_birth or "",
                "height": str(client.height) if client.height else "",
                "contactNumber": client.contact_number or "",
                "numberOfDependents": str(client.no_of_dependents) if client.no_of_dependents else "",
                "maritalStatus": reverse_map_marital_status(client.marital_status),
                "nationality": client.nationality or "",
                "weight": str(client.weight) if client.weight else "",
                "education": client.education or "",
                "spouseName": client.spouse_name or "",
                "spouseBirthDate": format_date_to_iso(client.spouse_birthdate),
                "spouseWork": client.work or "",
                "spouseMonthlyIncome": str(client.monthly_income) if client.monthly_income else "",
                
                # Address information
                "streetAddress": address.street if address else "",
                "barangay": address.barangay if address else "",
                "cityMunicipality": address.city_municipality if address else "",
                "province": address.province if address else "",
                "region": address.region if address else "",
                
                # Beneficiaries
                "beneficiaries": [
                    {
                        "name": beneficiary.name or "",
                        "birthDate": format_date_to_iso(beneficiary.birthdate),
                        "age": str(beneficiary.age) if beneficiary.age else "",
                        "relationship": beneficiary.relationship or ""
                    }
                    for beneficiary in beneficiaries
                ],
                
                # Co-Insured
                "coInsured": [
                    {
                        "name": co_ins.name or "",
                        "birthDate": format_date_to_iso(co_ins.birthdate),
                        "age": str(co_ins.age) if co_ins.age else "",
                        "relationship": co_ins.relationship or ""
                    }
                    for co_ins in co_insured
                ],
                
                # Income data (if available)
                "incomes": [
                    {
                        "type": income.type or "",
                        "frequency": income.frequency or "",
                        "amount": str(income.amount) if income.amount else "",
                        "description": income.description or ""
                    }
                    for income in incomes
                ],
                
                # Expense data (if available)
                "expenses": [
                    {
                        "type": expense.type or "",
                        "frequency": expense.frequency or "",
                        "amount": str(expense.amount) if expense.amount else "",
                        "description": expense.description or ""
                    }
                    for expense in expenses
                ]
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@client_bp.route('/clients', methods=['GET'])
def get_all_clients():
    try:
        # Import models inside the function to avoid circular imports
        from models import Client
        
        # Fetch all clients with only necessary fields
        clients = Client.query.with_entities(
            Client.id,
            Client.salutation,
            Client.first_name,
            Client.middle_name,
            Client.last_name
        ).all()
        
        # Format the response
        clients_list = []
        for client in clients:
            # Build full name
            name_parts = []
            if client.salutation:
                name_parts.append(client.salutation)
            if client.first_name:
                name_parts.append(client.first_name)
            if client.middle_name:
                name_parts.append(client.middle_name)
            if client.last_name:
                name_parts.append(client.last_name)
            
            full_name = " ".join(name_parts)
            
            clients_list.append({
                "id": client.id,
                "name": full_name,
                "firstName": client.first_name or "",
                "middleName": client.middle_name or "",
                "lastName": client.last_name or "",
                "salutation": client.salutation or ""
            })
        
        return jsonify({
            "clients": clients_list,
            "total_count": len(clients_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def map_salutation(salutation):
    """Map salutation from form to database enum"""
    mapping = {
        'mr': 'Mr.',
        'ms': 'Ms.',
        'mrs': 'Ms.',  # Assuming Mrs. maps to Ms.
        'others': 'Others'
    }
    return mapping.get(salutation.lower(), 'Others')

def map_gender(gender):
    """Map gender from form to database enum"""
    mapping = {
        'male': 'Male',
        'female': 'Female',
        'other': 'Other'
    }
    return mapping.get(gender.lower(), 'Other')

def map_marital_status(status):
    """Map marital status from form to database enum"""
    mapping = {
        'single': 'Single',
        'married': 'Married',
        'divorced': 'Divorced',
        'widowed': 'Widowed',
        'separated': 'Separated',
        'other': 'Other'
    }
    return mapping.get(status.lower(), 'Other')

def parse_date(date_string):
    """Parse ISO date string to date object"""
    if not date_string:
        return None
    try:
        # Parse ISO format date
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.date()
    except:
        return None

def parse_decimal(value):
    """Parse string to decimal, return None if invalid"""
    if not value:
        return None
    try:
        return float(value)
    except:
        return None

def parse_int(value):
    """Parse string to integer, return None if invalid"""
    if not value:
        return None
    try:
        return int(value)
    except:
        return None

def reverse_map_salutation(salutation):
    """Map salutation from database enum to form format"""
    mapping = {
        'Mr.': 'mr',
        'Ms.': 'ms',
        'Others': 'others'
    }
    return mapping.get(salutation, 'others')

def reverse_map_gender(gender):
    """Map gender from database enum to form format"""
    mapping = {
        'Male': 'male',
        'Female': 'female',
        'Other': 'other'
    }
    return mapping.get(gender, 'other')

def reverse_map_marital_status(status):
    """Map marital status from database enum to form format"""
    mapping = {
        'Single': 'single',
        'Married': 'married',
        'Divorced': 'divorced',
        'Widowed': 'widowed',
        'Separated': 'separated',
        'Other': 'other'
    }
    return mapping.get(status, 'other')

def format_date_to_iso(date_obj):
    """Format date object to ISO string"""
    if not date_obj:
        return ""
    try:
        # Convert date to datetime at midnight UTC and format as ISO
        dt = datetime.combine(date_obj, datetime.min.time())
        return dt.isoformat() + ".000Z"
    except:
        return ""