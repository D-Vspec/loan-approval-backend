from flask import request, jsonify
from datetime import datetime

def process_assessment_data_route(db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory, 
                                 LendingGroups, CenterStatusMembers, MeetingAttendance, 
                                 ProgramBenefitsReceived, YearsInProgram, PastdueRatio):
    def process_assessment_data():
        try:
            json_data = request.get_json()
            if not json_data or 'data' not in json_data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            client_id = json_data.get('clientId')
            data = json_data['data']
            
            # Validate client exists
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            # Delete existing assessment data for the client to replace with new data
            existing_records = [
                TimeInProgram.query.filter_by(client_id=client_id).all(),
                CenterCollectionRecord.query.filter_by(client_id=client_id).all(),
                PaymentHistory.query.filter_by(client_id=client_id).all(),
                LendingGroups.query.filter_by(client_id=client_id).all(),
                CenterStatusMembers.query.filter_by(client_id=client_id).all(),
                MeetingAttendance.query.filter_by(client_id=client_id).all(),
                ProgramBenefitsReceived.query.filter_by(client_id=client_id).all(),
                YearsInProgram.query.filter_by(client_id=client_id).all(),
                PastdueRatio.query.filter_by(client_id=client_id).all()
            ]
            
            for record_list in existing_records:
                for record in record_list:
                    db.session.delete(record)
            
            # Map the numeric values to enum values
            def map_time_in_program(value):
                mapping = {
                    '1': 'SecondCycleOrEarlier',
                    '2': 'ThirdToFourthCycle', 
                    '3': 'FifthToSixthCycle',
                    '4': 'SeventhToEighthCycle',
                    '5': 'NinthCycleAndBeyond'
                }
                return mapping.get(str(value), 'SecondCycleOrEarlier')
            
            def map_collection_record(value):
                mapping = {
                    '1': 'WeeklyPaymentsNotCompleted',
                    '2': 'PaymentsIncompleteDueDateCompletedWithinWeek',
                    '3': 'PaymentsCompletedMoreThan2hrsLateAfterADFollowup',
                    '4': 'PaymentsCompletedOnTime',
                    '5': 'PaymentsCompletedWithinSchedulePromptly'
                }
                return mapping.get(str(value), 'WeeklyPaymentsNotCompleted')
            
            def map_payment_history(value):
                mapping = {
                    '1': 'NoWeeklyPaymentsNotCoveredByOthers',
                    '2': 'OneToTwoRedMarksInPassbook',
                    '3': 'CoveredByCenterWithinTime',
                    '4': 'WeeklyContributionsUpToDate',
                    '5': 'PersonallyPaysOnTime'
                }
                return mapping.get(str(value), 'NoWeeklyPaymentsNotCoveredByOthers')
            
            def map_lending_groups(value):
                mapping = {
                    '1': 'NoExperienceWithLoanGroup',
                    '2': 'MemberOfMoreThan4Groups',
                    '3': 'MemberOf3To4Groups',
                    '4': 'SpouseMemberOfAnotherGroup',
                    '5': 'MemberOf1To2Groups'
                }
                return mapping.get(str(value), 'NoExperienceWithLoanGroup')
            
            def map_center_members(value):
                mapping = {
                    '1': 'FiveToTenMembers',
                    '2': 'ElevenToFifteenMembers',
                    '3': 'SixteenToTwentyMembers',
                    '4': 'TwentyOneToTwentyFiveMembers',
                    '5': 'TwentySixOrMoreMembers'
                }
                return mapping.get(str(value), 'FiveToTenMembers')
            
            def map_meeting_attendance(value):
                mapping = {
                    '1': 'AttendedOnceIn6Months',
                    '2': 'AttendedTwiceIn6Months',
                    '3': 'Attended3TimesIn6Months',
                    '4': 'Attended4TimesIn6Months',
                    '5': 'Attended5OrMoreTimesIn6Months'
                }
                return mapping.get(str(value), 'AttendedOnceIn6Months')
            
            def map_program_benefits(value):
                mapping = {
                    '1': 'NoBenefitsReceived',
                    '2': 'ReceivedOnlyOneBenefit',
                    '3': 'ReceivedTwoOrMoreBenefits'
                }
                return mapping.get(str(value), 'NoBenefitsReceived')
            
            def map_years_in_program(value):
                mapping = {
                    '1': 'TwoYearsOrLess',
                    '2': 'ThreeToFourYears',
                    '3': 'FiveToSixYears',
                    '4': 'SixToSevenYears',
                    '5': 'EightYearsOrMore'
                }
                return mapping.get(str(value), 'TwoYearsOrLess')
            
            def map_pastdue_ratio(value):
                mapping = {
                    '1': 'FourPercentOrHigher',
                    '2': 'ThreePercent',
                    '3': 'TwoPercent',
                    '4': 'OnePercent',
                    '5': 'ZeroPercentNoPastDue'
                }
                return mapping.get(str(value), 'FourPercentOrHigher')
            
            # Create new assessment records
            
            # Time in Program
            if data.get('timeInProgram'):
                time_in_program = TimeInProgram()
                time_in_program.client_id = client_id
                time_in_program.program_cycle = map_time_in_program(data['timeInProgram'])
                time_in_program.score = int(data['timeInProgram'])
                db.session.add(time_in_program)
            
            # Center Collection Record
            if data.get('centerCollectionRecord'):
                collection_record = CenterCollectionRecord()
                collection_record.client_id = client_id
                collection_record.collection_status = map_collection_record(data['centerCollectionRecord'])
                collection_record.score = int(data['centerCollectionRecord'])
                db.session.add(collection_record)
            
            # Payment History
            if data.get('paymentHistory'):
                payment_history = PaymentHistory()
                payment_history.client_id = client_id
                payment_history.payment_status = map_payment_history(data['paymentHistory'])
                payment_history.score = int(data['paymentHistory'])
                db.session.add(payment_history)
            
            # Number of Lending Groups
            if data.get('numberOfLendingGroups'):
                lending_group = LendingGroups()
                lending_group.client_id = client_id
                lending_group.group_participation = map_lending_groups(data['numberOfLendingGroups'])
                lending_group.score = int(data['numberOfLendingGroups'])
                db.session.add(lending_group)
            
            # Number of Center Members
            if data.get('numberOfCenterMembers'):
                center_member = CenterStatusMembers()
                center_member.client_id = client_id
                center_member.member_count = map_center_members(data['numberOfCenterMembers'])
                center_member.score = int(data['numberOfCenterMembers'])
                db.session.add(center_member)
            
            # Attendance to Meetings
            if data.get('attendanceToMeetings'):
                meeting_attendance = MeetingAttendance()
                meeting_attendance.client_id = client_id
                meeting_attendance.attendance_frequency = map_meeting_attendance(data['attendanceToMeetings'])
                meeting_attendance.score = int(data['attendanceToMeetings'])
                db.session.add(meeting_attendance)
            
            # Program Benefits Received
            if data.get('programBenefitsReceived'):
                program_benefits = ProgramBenefitsReceived()
                program_benefits.client_id = client_id
                program_benefits.benefits_received = map_program_benefits(data['programBenefitsReceived'])
                program_benefits.score = int(data['programBenefitsReceived'])
                db.session.add(program_benefits)
            
            # Years in Program
            if data.get('yearsInProgram'):
                years_in_program = YearsInProgram()
                years_in_program.client_id = client_id
                years_in_program.program_duration = map_years_in_program(data['yearsInProgram'])
                years_in_program.score = int(data['yearsInProgram'])
                db.session.add(years_in_program)
            
            # Pastdue Ratio
            if data.get('pastdueRatio'):
                pastdue_ratio = PastdueRatio()
                pastdue_ratio.client_id = client_id
                pastdue_ratio.ratio_category = map_pastdue_ratio(data['pastdueRatio'])
                pastdue_ratio.score = int(data['pastdueRatio'])
                db.session.add(pastdue_ratio)
            
            # Commit all changes
            db.session.commit()
            
            # Calculate total score
            total_score = 0
            for field in ['timeInProgram', 'centerCollectionRecord', 'paymentHistory', 
                         'numberOfLendingGroups', 'numberOfCenterMembers', 'attendanceToMeetings',
                         'programBenefitsReceived', 'yearsInProgram', 'pastdueRatio']:
                if data.get(field):
                    total_score += int(data[field])
            
            return jsonify({
                'message': 'Assessment data processed successfully',
                'client_id': client_id,
                'assessment_date': data.get('assessmentDate'),
                'remarks': data.get('remarks'),
                'total_score': total_score,
                'individual_scores': {
                    'timeInProgram': int(data.get('timeInProgram', 0)),
                    'centerCollectionRecord': int(data.get('centerCollectionRecord', 0)),
                    'paymentHistory': int(data.get('paymentHistory', 0)),
                    'numberOfLendingGroups': int(data.get('numberOfLendingGroups', 0)),
                    'numberOfCenterMembers': int(data.get('numberOfCenterMembers', 0)),
                    'attendanceToMeetings': int(data.get('attendanceToMeetings', 0)),
                    'programBenefitsReceived': int(data.get('programBenefitsReceived', 0)),
                    'yearsInProgram': int(data.get('yearsInProgram', 0)),
                    'pastdueRatio': int(data.get('pastdueRatio', 0))
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    return process_assessment_data
