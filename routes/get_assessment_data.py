from flask import jsonify

def get_assessment_data_route(Client, TimeInProgram, CenterCollectionRecord, PaymentHistory,
                              LendingGroups, CenterStatusMembers, MeetingAttendance,
                              ProgramBenefitsReceived, YearsInProgram, PastdueRatio):
    def get_assessment_data(client_id):
        try:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

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
                "recordAssessment": {
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
                    ]
                },
                "centerStatusAssessment": {
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
                            "benefitsReceived": benefit.benefits_name.value if benefit.benefits_name else ""
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
    return get_assessment_data
