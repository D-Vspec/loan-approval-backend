from flask import jsonify, request
from .utils import reverse_map_salutation, reverse_map_gender, reverse_map_marital_status, format_date_to_iso

def get_client_details_route(Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense,
                            PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis, Residency,
                            FamilyAndToiletStatus, TimeInProgram, CenterCollectionRecord, PaymentHistory,
                            LendingGroups, CenterStatusMembers, MeetingAttendance, ProgramBenefitsReceived,
                            YearsInProgram, PastdueRatio):
    def get_client_details(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            address = AddressInformation.query.filter_by(client_id=client_id).first()
            beneficiaries = Beneficiaries.query.filter_by(client_id=client_id).all()
            co_insured = CoInsured.query.filter_by(client_id=client_id).all()
            incomes = Income.query.filter_by(client_id=client_id).all()
            expenses = Expense.query.filter_by(client_id=client_id).all()
            primary_repayment_sources = PrimaryRepaymentSource.query.filter_by(client_id=client_id).all()
            other_repayment_sources = OtherRepaymentSource.query.filter_by(client_id=client_id).all()
            cash_flow_analyses = CashFlowAnalysis.query.filter_by(client_id=client_id).all()
            residencies = Residency.query.filter_by(client_id=client_id).all()
            family_toilet_statuses = FamilyAndToiletStatus.query.filter_by(client_id=client_id).all()
            # Pick first (latest inserted) entries for simple field mapping
            residency_single = residencies[0] if residencies else None
            family_toilet_single = family_toilet_statuses[0] if family_toilet_statuses else None
            time_in_programs = TimeInProgram.query.filter_by(client_id=client_id).all()
            collection_records = CenterCollectionRecord.query.filter_by(client_id=client_id).all()
            payment_histories = PaymentHistory.query.filter_by(client_id=client_id).all()
            lending_groups = LendingGroups.query.filter_by(client_id=client_id).all()
            center_members = CenterStatusMembers.query.filter_by(client_id=client_id).all()
            meeting_attendances = MeetingAttendance.query.filter_by(client_id=client_id).all()
            program_benefits = ProgramBenefitsReceived.query.filter_by(client_id=client_id).all()
            years_in_program = YearsInProgram.query.filter_by(client_id=client_id).all()
            pastdue_ratios = PastdueRatio.query.filter_by(client_id=client_id).all()
            response_data = {
                "submissionDate": format_date_to_iso(client.birthdate),
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
                    "typeOfLoan": client.type_of_loan or "",
                    "loanAmount": str(client.loan_amount) if client.loan_amount else "",
                    "verified": client.verified,
                    # Added single-value residency & family/toilet fields
                    "lengthOfStay": residency_single.length_of_stay.value if residency_single and residency_single.length_of_stay else "",
                    "lengthOfStayCustom": residency_single.length_of_stay_custom if residency_single and residency_single.length_of_stay_custom else "",
                    "ownershipOfResidence": residency_single.ownership_type.value if residency_single and residency_single.ownership_type else "",
                    "ownershipOfResidenceCustom": residency_single.ownership_type_custom if residency_single and residency_single.ownership_type_custom else "",
                    "familyStatus": family_toilet_single.family_status.value if family_toilet_single and family_toilet_single.family_status else "",
                    "familyStatusCustom": family_toilet_single.family_status_custom if family_toilet_single and family_toilet_single.family_status_custom else "",
                    "toiletStatus": family_toilet_single.toilet_status.value if family_toilet_single and family_toilet_single.toilet_status else "",
                    "toiletStatusCustom": family_toilet_single.toilet_status_custom if family_toilet_single and family_toilet_single.toilet_status_custom else "",
                    "streetAddress": address.street if address else "",
                    "barangay": address.barangay if address else "",
                    "cityMunicipality": address.city_municipality if address else "",
                    "province": address.province if address else "",
                    "region": address.region if address else "",
                    "beneficiaries": [
                        {
                            "name": beneficiary.name or "",
                            "birthDate": format_date_to_iso(beneficiary.birthdate),
                            "age": str(beneficiary.age) if beneficiary.age else "",
                            "relationship": beneficiary.relationship or ""
                        }
                        for beneficiary in beneficiaries
                    ],
                    "coInsured": [
                        {
                            "name": co_ins.name or "",
                            "birthDate": format_date_to_iso(co_ins.birthdate),
                            "age": str(co_ins.age) if co_ins.age else "",
                            "relationship": co_ins.relationship or ""
                        }
                        for co_ins in co_insured
                    ],
                    "incomes": [
                        {
                            "type": income.type.value if income.type else "",
                            "frequency": income.frequency.value if income.frequency else "",
                            "amount": str(income.amount) if income.amount else "",
                            "description": income.description or ""
                        }
                        for income in incomes
                    ],
                    "expenses": [
                        {
                            "type": expense.type.value if expense.type else "",
                            "frequency": expense.frequency.value if expense.frequency else "",
                            "amount": str(expense.amount) if expense.amount else "",
                            "description": expense.description or ""
                        }
                        for expense in expenses
                    ],
                    "primaryRepaymentSources": [
                        {
                            "sourceType": source.source_type.value if source.source_type else "",
                            "customDescription": source.custom_description or "",
                            "score": source.score or 0
                        }
                        for source in primary_repayment_sources
                    ],
                    "otherRepaymentSources": [
                        {
                            "sourceType": source.source_type.value if source.source_type else "",
                            "customDescription": source.custom_description or "",
                            "points": source.points or 0
                        }
                        for source in other_repayment_sources
                    ],
                    "cashFlowAnalyses": [
                        {
                            "weeklyCashFlow": str(analysis.weekly_cash_flow) if analysis.weekly_cash_flow else "",
                            "cashFlowCategory": analysis.cash_flow_category.value if analysis.cash_flow_category else "",
                            "desiredWeeklyInstallment": str(analysis.desired_weekly_installment) if analysis.desired_weekly_installment else "",
                            "score": analysis.score or 0
                        }
                        for analysis in cash_flow_analyses
                    ],
                    "residencies": [
                        {
                            "lengthOfStay": residency.length_of_stay.value if residency.length_of_stay else "",
                            "lengthOfStayCustom": residency.length_of_stay_custom or "",
                            "ownershipType": residency.ownership_type.value if residency.ownership_type else "",
                            "ownershipTypeCustom": residency.ownership_type_custom or "",
                            "score": residency.score or 0
                        }
                        for residency in residencies
                    ],
                    "familyAndToiletStatuses": [
                        {
                            "familyStatus": status.family_status.value if status.family_status else "",
                            "familyStatusCustom": status.family_status_custom or "",
                            "toiletStatus": status.toilet_status.value if status.toilet_status else "",
                            "toiletStatusCustom": status.toilet_status_custom or "",
                            "score": status.score or 0
                        }
                        for status in family_toilet_statuses
                    ],
                    "timeInPrograms": [
                        {
                            "programCycle": program.program_cycle.value if program.program_cycle else "",
                            "customDescription": program.custom_description or "",
                            "score": program.score or 0
                        }
                        for program in time_in_programs
                    ],
                    "centerCollectionRecords": [
                        {
                            "collectionStatus": record.collection_status.value if record.collection_status else "",
                            "customDescription": record.custom_description or "",
                            "score": record.score or 0
                        }
                        for record in collection_records
                    ],
                    "paymentHistories": [
                        {
                            "paymentStatus": history.payment_status.value if history.payment_status else "",
                            "customDescription": history.custom_description or "",
                            "score": history.score or 0
                        }
                        for history in payment_histories
                    ],
                    "lendingGroups": [
                        {
                            "groupParticipation": group.group_participation.value if group.group_participation else "",
                            "customDescription": group.custom_description or "",
                            "score": group.score or 0
                        }
                        for group in lending_groups
                    ],
                    "centerStatusMembers": [
                        {
                            "memberCount": member.member_count.value if member.member_count else "",
                            "customDescription": member.custom_description or "",
                            "score": member.score or 0
                        }
                        for member in center_members
                    ],
                    "meetingAttendances": [
                        {
                            "attendanceFrequency": attendance.attendance_frequency.value if attendance.attendance_frequency else "",
                            "customDescription": attendance.custom_description or "",
                            "score": attendance.score or 0
                        }
                        for attendance in meeting_attendances
                    ],
                    "programBenefitsReceived": [
                        {
                            "benefitsReceived": benefit.benefits_received.value if benefit.benefits_received else "",
                            "customDescription": benefit.custom_description or "",
                            "score": benefit.score or 0
                        }
                        for benefit in program_benefits
                    ],
                    "yearsInProgram": [
                        {
                            "programDuration": years.program_duration.value if years.program_duration else "",
                            "customDescription": years.custom_description or "",
                            "score": years.score or 0
                        }
                        for years in years_in_program
                    ],
                    "pastdueRatios": [
                        {
                            "ratioCategory": ratio.ratio_category.value if ratio.ratio_category else "",
                            "customDescription": ratio.custom_description or "",
                            "score": ratio.score or 0
                        }
                        for ratio in pastdue_ratios
                    ]
                }
            }
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    return get_client_details
