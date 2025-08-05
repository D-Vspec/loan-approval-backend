from flask import Blueprint, request, jsonify
from .utils import map_salutation, map_gender, map_marital_status, parse_date, parse_decimal, parse_int, map_other_repayment_source, map_primary_repayment_source

def process_form_data_route(db, Client, AddressInformation, Beneficiaries, CoInsured, PrimaryRepaymentSource, OtherRepaymentSource):
    def process_form_data():
        try:
            json_data = request.get_json()
            if not json_data or 'data' not in json_data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            data = json_data['data']
            
            print("Processing form data:", data)  # Debugging line
            
            client = Client()
            client.salutation = map_salutation(data.get('salutation', ''))
            client.last_name = data.get('lastName', '')
            client.first_name = data.get('firstName', '')
            client.middle_name = data.get('middleName', '')
            
            print("Client created with name:", client.first_name, client.last_name)  # Debugging line
            
            client.gender = map_gender(data.get('gender', ''))
            client.birthdate = parse_date(data.get('birthDate'))
            client.place_of_birth = data.get('placeOfBirth', '')
            client.height = parse_decimal(data.get('height'))
            client.contact_number = data.get('contactNumber', '')
            
            print("Client contact number:", client.contact_number)  # Debugging line
            
            client.no_of_dependents = parse_int(data.get('numberOfDependents'))
            client.marital_status = map_marital_status(data.get('maritalStatus', ''))
            client.nationality = data.get('nationality', '')
            client.weight = parse_decimal(data.get('weight'))
            client.education = data.get('education', '')
            client.spouse_name = data.get('spouseName', '')
            client.spouse_birthdate = parse_date(data.get('spouseBirthDate'))
            client.work = data.get('spouseWork', '')
            client.monthly_income = parse_decimal(data.get('spouseMonthlyIncome'))
            print("Client spouse information:", client.spouse_name, client.spouse_birthdate)  # Debugging line
            db.session.add(client)
            print("Client created:", client.id)  # Debugging line
            db.session.flush()
            address = AddressInformation()
            address.client_id = client.id
            address.street = data.get('streetAddress', '')
            address.barangay = data.get('barangay', '')
            address.city_municipality = data.get('cityMunicipality', '')
            address.province = data.get('province', '')
            address.region = data.get('region', '')
            db.session.add(address)
            print("Address added for client:", client.id)  # Debugging line
            beneficiaries_data = data.get('beneficiaries', [])
            for beneficiary_data in beneficiaries_data:
                beneficiary = Beneficiaries()
                beneficiary.client_id = client.id
                beneficiary.name = beneficiary_data.get('name', '')
                beneficiary.birthdate = parse_date(beneficiary_data.get('birthDate'))
                beneficiary.age = parse_int(beneficiary_data.get('age'))
                beneficiary.relationship = beneficiary_data.get('relationship', '')
                db.session.add(beneficiary)
            co_insured_data = data.get('coInsured', [])
            for co_insured_item in co_insured_data:
                co_insured = CoInsured()
                co_insured.client_id = client.id
                co_insured.name = co_insured_item.get('name', '')
                co_insured.birthdate = parse_date(co_insured_item.get('birthDate'))
                co_insured.age = parse_int(co_insured_item.get('age'))
                co_insured.relationship = co_insured_item.get('relationship', '')
                db.session.add(co_insured)
            # Handle primary loan repayment sources
            primary_loan_repayment = data.get('primaryLoanRepayment', [])
            for source in primary_loan_repayment:
                primary_source = PrimaryRepaymentSource()
                primary_source.client_id = client.id
                
                # Check if source is a dictionary (for "other" with comment)
                if isinstance(source, dict):
                    primary_source.source_type = map_primary_repayment_source(source.get('value', ''))
                    primary_source.custom_description = source.get('comment', '')
                else:
                    primary_source.source_type = map_primary_repayment_source(source)  # map to enum value
                    primary_source.custom_description = None
                
                db.session.add(primary_source)

            # Handle other loan repayment sources
            other_loan_repayment = data.get('otherLoanRepayment', [])
            for source in other_loan_repayment:
                other_source = OtherRepaymentSource()
                other_source.client_id = client.id
                
                if isinstance(source, dict):
                    other_source.source_type = map_other_repayment_source(source.get('value', ''))
                    other_source.custom_description = source.get('comment', '')
                else:
                    other_source.source_type = map_other_repayment_source(source)  # map to enum value
                    other_source.custom_description = None
                
                db.session.add(other_source)
            db.session.commit()
            return jsonify({
                'message': 'Client data processed successfully',
                'client_id': client.id,
                'submission_date': json_data.get('submissionDate'),
                'form_type': json_data.get('formType')
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    return process_form_data
