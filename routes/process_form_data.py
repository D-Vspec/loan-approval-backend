from flask import Blueprint, request, jsonify
from .utils import (map_salutation, map_gender, map_marital_status, parse_date, parse_decimal, parse_int, 
                   map_other_repayment_source, map_primary_repayment_source, map_income_expense_type, map_frequency)
from models import LengthOfStayEnum, OwnershipTypeEnum, FamilyStatusEnum, ToiletStatusEnum

def process_form_data_route(db, Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense, PrimaryRepaymentSource, OtherRepaymentSource, Residency, FamilyAndToiletStatus):
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
            client.type_of_loan = data.get('typeOfLoan', '')
            client.loan_amount = parse_decimal(data.get('loanAmount'))
            
            print("Client spouse information:", client.spouse_name, client.spouse_birthdate)  # Debugging line
            print("Loan information:", client.type_of_loan, client.loan_amount)  # Debugging line
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
            
            # Handle business income
            business_income_data = data.get('businessIncome', [])
            for income_item in business_income_data:
                # Process each frequency type that has a value
                for freq_key, freq_value in income_item.items():
                    if freq_key != 'description' and freq_value and freq_value.strip():
                        income = Income()
                        income.client_id = client.id
                        income.type = map_income_expense_type('business')
                        income.frequency = map_frequency(freq_key)
                        income.amount = parse_decimal(freq_value)
                        income.description = income_item.get('description', '')
                        db.session.add(income)
            
            # Handle household income
            household_income_data = data.get('householdIncome', [])
            for income_item in household_income_data:
                # Process each frequency type that has a value
                for freq_key, freq_value in income_item.items():
                    if freq_key != 'description' and freq_value and freq_value.strip():
                        income = Income()
                        income.client_id = client.id
                        income.type = map_income_expense_type('household')
                        income.frequency = map_frequency(freq_key)
                        income.amount = parse_decimal(freq_value)
                        income.description = income_item.get('description', '')
                        db.session.add(income)
            
            # Handle business expenses
            business_expenses_data = data.get('businessExpenses', [])
            for expense_item in business_expenses_data:
                # Process each frequency type that has a value
                for freq_key, freq_value in expense_item.items():
                    if freq_key != 'description' and freq_value and freq_value.strip():
                        expense = Expense()
                        expense.client_id = client.id
                        expense.type = map_income_expense_type('business')
                        expense.frequency = map_frequency(freq_key)
                        expense.amount = parse_decimal(freq_value)
                        expense.description = expense_item.get('description', '')
                        db.session.add(expense)
            
            # Handle household expenses
            household_expenses_data = data.get('householdExpenses', [])
            for expense_item in household_expenses_data:
                # Process each frequency type that has a value
                for freq_key, freq_value in expense_item.items():
                    if freq_key != 'description' and freq_value and freq_value.strip():
                        expense = Expense()
                        expense.client_id = client.id
                        expense.type = map_income_expense_type('household')
                        expense.frequency = map_frequency(freq_key)
                        expense.amount = parse_decimal(freq_value)
                        expense.description = expense_item.get('description', '')
                        db.session.add(expense)
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

            # NEW: Handle residency (length of stay and ownership)
            length_of_stay_val = data.get('lengthOfStay')
            ownership_val = data.get('ownershipOfResidence')
            if length_of_stay_val or ownership_val:
                if not (length_of_stay_val and ownership_val):
                    db.session.rollback()
                    return jsonify({'error': 'Both lengthOfStay and ownershipOfResidence are required together.'}), 400
                residency = Residency()
                residency.client_id = client.id
                try:
                    residency.length_of_stay = LengthOfStayEnum(length_of_stay_val)
                except ValueError:
                    residency.length_of_stay = LengthOfStayEnum.Other
                    if length_of_stay_val != 'other':
                        residency.length_of_stay_custom = length_of_stay_val  # preserve unexpected value
                if length_of_stay_val == 'other':
                    residency.length_of_stay_custom = data.get('lengthOfStayCustom', '')
                try:
                    residency.ownership_type = OwnershipTypeEnum(ownership_val)
                except ValueError:
                    residency.ownership_type = OwnershipTypeEnum.Other
                    if ownership_val != 'other':
                        residency.ownership_type_custom = ownership_val
                if ownership_val == 'other':
                    residency.ownership_type_custom = data.get('ownershipOfResidenceCustom', '')
                db.session.add(residency)

            # NEW: Handle family and toilet status
            family_status_val = data.get('familyStatus')
            toilet_status_val = data.get('toiletStatus')
            if family_status_val or toilet_status_val:
                if not (family_status_val and toilet_status_val):
                    db.session.rollback()
                    return jsonify({'error': 'Both familyStatus and toiletStatus are required together.'}), 400
                family_toilet = FamilyAndToiletStatus()
                family_toilet.client_id = client.id
                try:
                    family_toilet.family_status = FamilyStatusEnum(family_status_val)
                except ValueError:
                    family_toilet.family_status = FamilyStatusEnum.Other
                    if family_status_val != 'other':
                        family_toilet.family_status_custom = family_status_val
                if family_status_val == 'other':
                    family_toilet.family_status_custom = data.get('familyStatusCustom', '')
                try:
                    family_toilet.toilet_status = ToiletStatusEnum(toilet_status_val)
                except ValueError:
                    family_toilet.toilet_status = ToiletStatusEnum.Other
                    if toilet_status_val != 'other':
                        family_toilet.toilet_status_custom = toilet_status_val
                if toilet_status_val == 'other':
                    family_toilet.toilet_status_custom = data.get('toiletStatusCustom', '')
                db.session.add(family_toilet)

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
