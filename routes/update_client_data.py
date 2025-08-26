from flask import jsonify, request
from .utils import (
    map_salutation, map_gender, map_marital_status, parse_date, parse_decimal, parse_int,
    map_other_repayment_source, map_primary_repayment_source, map_income_expense_type, map_frequency
)

def update_client_data_route(db, Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense, PrimaryRepaymentSource, OtherRepaymentSource):
    def update_client_data(client_id):
        try:
            json_data = request.get_json()
            if not json_data or 'data' not in json_data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            data = json_data['data']

            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

            # Basic scalar fields (only update if key present to allow partial updates)
            if 'salutation' in data:
                client.salutation = map_salutation(data.get('salutation'))
            if 'lastName' in data:
                client.last_name = data.get('lastName') or ''
            if 'firstName' in data:
                client.first_name = data.get('firstName') or ''
            if 'middleName' in data:
                client.middle_name = data.get('middleName') or ''
            if 'gender' in data:
                client.gender = map_gender(data.get('gender') or '')
            if 'birthDate' in data:
                client.birthdate = parse_date(data.get('birthDate'))
            if 'placeOfBirth' in data:
                client.place_of_birth = data.get('placeOfBirth') or ''
            if 'height' in data:
                client.height = parse_decimal(data.get('height'))
            if 'contactNumber' in data:
                client.contact_number = data.get('contactNumber') or ''
            if 'numberOfDependents' in data:
                client.no_of_dependents = parse_int(data.get('numberOfDependents'))
            if 'maritalStatus' in data:
                client.marital_status = map_marital_status(data.get('maritalStatus') or '')
            if 'nationality' in data:
                client.nationality = data.get('nationality') or ''
            if 'weight' in data:
                client.weight = parse_decimal(data.get('weight'))
            if 'education' in data:
                client.education = data.get('education') or ''
            if 'spouseName' in data:
                client.spouse_name = data.get('spouseName') or ''
            if 'spouseBirthDate' in data:
                client.spouse_birthdate = parse_date(data.get('spouseBirthDate'))
            if 'spouseWork' in data:
                client.work = data.get('spouseWork') or ''
            if 'spouseMonthlyIncome' in data:
                client.monthly_income = parse_decimal(data.get('spouseMonthlyIncome'))
            if 'typeOfLoan' in data:
                client.type_of_loan = data.get('typeOfLoan') or ''
            if 'loanAmount' in data:
                client.loan_amount = parse_decimal(data.get('loanAmount'))

            # Address (replace if provided)
            if any(k in data for k in ['streetAddress', 'barangay', 'cityMunicipality', 'province', 'region']):
                address = AddressInformation.query.filter_by(client_id=client.id).first()
                if not address:
                    address = AddressInformation(client_id=client.id)
                    db.session.add(address)
                if 'streetAddress' in data:
                    address.street = data.get('streetAddress') or ''
                if 'barangay' in data:
                    address.barangay = data.get('barangay') or ''
                if 'cityMunicipality' in data:
                    address.city_municipality = data.get('cityMunicipality') or ''
                if 'province' in data:
                    address.province = data.get('province') or ''
                if 'region' in data:
                    address.region = data.get('region') or ''

            # Helpers to replace collections if provided
            def replace_collection(model_cls, items, builder):
                model_cls.query.filter_by(client_id=client.id).delete()
                for item in items:
                    obj = builder(item)
                    if obj:
                        db.session.add(obj)

            # Beneficiaries
            if 'beneficiaries' in data:
                beneficiaries_data = data.get('beneficiaries') or []
                def build_beneficiary(b):
                    ben = Beneficiaries()
                    ben.client_id = client.id
                    ben.name = b.get('name', '')
                    ben.birthdate = parse_date(b.get('birthDate'))
                    ben.age = parse_int(b.get('age'))
                    ben.relationship = b.get('relationship', '')
                    return ben
                replace_collection(Beneficiaries, beneficiaries_data, build_beneficiary)

            # Co-Insured
            if 'coInsured' in data:
                co_insured_data = data.get('coInsured') or []
                def build_co_insured(ci):
                    c = CoInsured()
                    c.client_id = client.id
                    c.name = ci.get('name', '')
                    c.birthdate = parse_date(ci.get('birthDate'))
                    c.age = parse_int(ci.get('age'))
                    c.relationship = ci.get('relationship', '')
                    return c
                replace_collection(CoInsured, co_insured_data, build_co_insured)

            # Business Income
            if 'businessIncome' in data:
                business_income_data = data.get('businessIncome') or []
                Income.query.filter_by(client_id=client.id, type='Business').delete()
                for income_item in business_income_data:
                    for freq_key, freq_value in income_item.items():
                        if freq_key != 'description' and freq_value and str(freq_value).strip():
                            inc = Income()
                            inc.client_id = client.id
                            inc.type = map_income_expense_type('business')
                            inc.frequency = map_frequency(freq_key)
                            inc.amount = parse_decimal(freq_value)
                            inc.description = income_item.get('description', '')
                            db.session.add(inc)

            # Household Income
            if 'householdIncome' in data:
                household_income_data = data.get('householdIncome') or []
                Income.query.filter_by(client_id=client.id, type='Household').delete()
                for income_item in household_income_data:
                    for freq_key, freq_value in income_item.items():
                        if freq_key != 'description' and freq_value and str(freq_value).strip():
                            inc = Income()
                            inc.client_id = client.id
                            inc.type = map_income_expense_type('household')
                            inc.frequency = map_frequency(freq_key)
                            inc.amount = parse_decimal(freq_value)
                            inc.description = income_item.get('description', '')
                            db.session.add(inc)

            # Business Expenses
            if 'businessExpenses' in data:
                business_expenses_data = data.get('businessExpenses') or []
                Expense.query.filter_by(client_id=client.id, type='Business').delete()
                for expense_item in business_expenses_data:
                    for freq_key, freq_value in expense_item.items():
                        if freq_key != 'description' and freq_value and str(freq_value).strip():
                            exp = Expense()
                            exp.client_id = client.id
                            exp.type = map_income_expense_type('business')
                            exp.frequency = map_frequency(freq_key)
                            exp.amount = parse_decimal(freq_value)
                            exp.description = expense_item.get('description', '')
                            db.session.add(exp)

            # Household Expenses
            if 'householdExpenses' in data:
                household_expenses_data = data.get('householdExpenses') or []
                Expense.query.filter_by(client_id=client.id, type='Household').delete()
                for expense_item in household_expenses_data:
                    for freq_key, freq_value in expense_item.items():
                        if freq_key != 'description' and freq_value and str(freq_value).strip():
                            exp = Expense()
                            exp.client_id = client.id
                            exp.type = map_income_expense_type('household')
                            exp.frequency = map_frequency(freq_key)
                            exp.amount = parse_decimal(freq_value)
                            exp.description = expense_item.get('description', '')
                            db.session.add(exp)

            # Primary Repayment Sources
            if 'primaryLoanRepayment' in data:
                PrimaryRepaymentSource.query.filter_by(client_id=client.id).delete()
                primary_loan_repayment = data.get('primaryLoanRepayment') or []
                for source in primary_loan_repayment:
                    ps = PrimaryRepaymentSource()
                    ps.client_id = client.id
                    if isinstance(source, dict):
                        ps.source_type = map_primary_repayment_source(source.get('value', ''))
                        ps.custom_description = source.get('comment', '')
                    else:
                        ps.source_type = map_primary_repayment_source(source)
                        ps.custom_description = None
                    db.session.add(ps)

            # Other Repayment Sources
            if 'otherLoanRepayment' in data:
                OtherRepaymentSource.query.filter_by(client_id=client.id).delete()
                other_loan_repayment = data.get('otherLoanRepayment') or []
                for source in other_loan_repayment:
                    os = OtherRepaymentSource()
                    os.client_id = client.id
                    if isinstance(source, dict):
                        os.source_type = map_other_repayment_source(source.get('value', ''))
                        os.custom_description = source.get('comment', '')
                    else:
                        os.source_type = map_other_repayment_source(source)
                        os.custom_description = None
                    db.session.add(os)

            db.session.commit()
            return jsonify({'message': 'Client data updated successfully', 'client_id': client.id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    return update_client_data
