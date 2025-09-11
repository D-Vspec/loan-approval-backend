from flask import request, jsonify
from datetime import datetime

def update_assessment_data_route(db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory, 
                                 LendingGroups, CenterStatusMembers, MeetingAttendance, 
                                 ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord):
    def update_assessment_data(client_id):
        try:
            json_data = request.get_json()
            if not json_data or 'data' not in json_data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            data = json_data['data']
            
            # Validate client exists
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
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
            
            def map_program_benefits(benefit_name):
                mapping = {
                    'gyrt_life_insurance': 'GYRT_LIFE_INSURANCE',
                    'cgl_loan_insurance': 'CGL_LOAN_INSURANCE',
                    'bya_medical_assistance': 'BYA_MEDICAL_ASSISTANCE',
                    'bya_educational_assistance': 'BYA_EDUCATIONAL_ASSISTANCE',
                    'none': 'NONE'
                }
                return mapping.get(benefit_name)

            def map_barangay_record(value):
                mapping = {
                    '1': 'SpouseOnlyKnown',
                    '2': 'BornAndNoRecord',
                    '3': 'ReputableFamily',
                    '4': 'RelativeInCouncil',
                    '5': 'FamilyElected'
                }
                if str(value) in mapping.values():
                    return value
                return mapping.get(str(value), 'SpouseOnlyKnown')

            # Update or create assessment records
            
            # Time in Program
            if data.get('timeInProgram'):
                time_in_program = TimeInProgram.query.filter_by(client_id=client_id).first()
                if not time_in_program:
                    time_in_program = TimeInProgram(client_id=client_id)
                    db.session.add(time_in_program)
                time_in_program.program_cycle = map_time_in_program(data['timeInProgram'])
                time_in_program.score = int(data['timeInProgram'])
            
            # Center Collection Record
            if data.get('centerCollectionRecord'):
                collection_record = CenterCollectionRecord.query.filter_by(client_id=client_id).first()
                if not collection_record:
                    collection_record = CenterCollectionRecord(client_id=client_id)
                    db.session.add(collection_record)
                collection_record.collection_status = map_collection_record(data['centerCollectionRecord'])
                collection_record.score = int(data['centerCollectionRecord'])
            
            # Payment History
            if data.get('paymentHistory'):
                payment_history = PaymentHistory.query.filter_by(client_id=client_id).first()
                if not payment_history:
                    payment_history = PaymentHistory(client_id=client_id)
                    db.session.add(payment_history)
                payment_history.payment_status = map_payment_history(data['paymentHistory'])
                payment_history.score = int(data['paymentHistory'])
            
            # Number of Lending Groups
            if data.get('numberOfLendingGroups'):
                lending_group = LendingGroups.query.filter_by(client_id=client_id).first()
                if not lending_group:
                    lending_group = LendingGroups(client_id=client_id)
                    db.session.add(lending_group)
                lending_group.group_participation = map_lending_groups(data['numberOfLendingGroups'])
                lending_group.score = int(data['numberOfLendingGroups'])
            
            # Number of Center Members
            if data.get('numberOfCenterMembers'):
                center_member = CenterStatusMembers.query.filter_by(client_id=client_id).first()
                if not center_member:
                    center_member = CenterStatusMembers(client_id=client_id)
                    db.session.add(center_member)
                center_member.member_count = map_center_members(data['numberOfCenterMembers'])
                center_member.score = int(data['numberOfCenterMembers'])
            
            # Attendance to Meetings
            if data.get('attendanceToMeetings'):
                meeting_attendance = MeetingAttendance.query.filter_by(client_id=client_id).first()
                if not meeting_attendance:
                    meeting_attendance = MeetingAttendance(client_id=client_id)
                    db.session.add(meeting_attendance)
                meeting_attendance.attendance_frequency = map_meeting_attendance(data['attendanceToMeetings'])
                meeting_attendance.score = int(data['attendanceToMeetings'])
            
            # Program Benefits Received - This is a list, so we clear existing and add new
            if 'programBenefitsReceived' in data and isinstance(data['programBenefitsReceived'], list):
                ProgramBenefitsReceived.query.filter_by(client_id=client_id).delete()
                for benefit_name in data['programBenefitsReceived']:
                    mapped_benefit = map_program_benefits(benefit_name)
                    if mapped_benefit:
                        program_benefit = ProgramBenefitsReceived(client_id=client_id, benefits_name=mapped_benefit)
                        db.session.add(program_benefit)
            
            # Years in Program
            if data.get('yearsInProgram'):
                years_in_program = YearsInProgram.query.filter_by(client_id=client_id).first()
                if not years_in_program:
                    years_in_program = YearsInProgram(client_id=client_id)
                    db.session.add(years_in_program)
                years_in_program.program_duration = map_years_in_program(data['yearsInProgram'])
                years_in_program.score = int(data['yearsInProgram'])
            
            # Pastdue Ratio
            if data.get('pastdueRatio'):
                pastdue_ratio = PastdueRatio.query.filter_by(client_id=client_id).first()
                if not pastdue_ratio:
                    pastdue_ratio = PastdueRatio(client_id=client_id)
                    db.session.add(pastdue_ratio)
                pastdue_ratio.ratio_category = map_pastdue_ratio(data['pastdueRatio'])
                pastdue_ratio.score = int(data['pastdueRatio'])
            
            # Barangay Record
            if data.get('barangayRecord'):
                barangay_record = BarangayRecord.query.filter_by(client_id=client_id).first()
                if not barangay_record:
                    barangay_record = BarangayRecord(client_id=client_id)
                    db.session.add(barangay_record)
                barangay_record.record_status = map_barangay_record(data['barangayRecord'])
                if str(data['barangayRecord']).isdigit():
                    barangay_record.score = int(data['barangayRecord'])
                else:
                    barangay_record.score = 0

            # Commit all changes
            db.session.commit()
            
            # Recalculate total score
            total_score = 0
            for field in ['timeInProgram', 'centerCollectionRecord', 'paymentHistory', 
                         'numberOfLendingGroups', 'numberOfCenterMembers', 'attendanceToMeetings',
                         'yearsInProgram', 'pastdueRatio', 'barangayRecord']:
                if data.get(field) and str(data[field]).isdigit():
                    total_score += int(data[field])
            
            return jsonify({
                'message': 'Assessment data updated successfully',
                'client_id': client_id,
                'total_score': total_score,
                'individual_scores': {
                    'timeInProgram': int(data.get('timeInProgram', 0)),
                    'centerCollectionRecord': int(data.get('centerCollectionRecord', 0)),
                    'paymentHistory': int(data.get('paymentHistory', 0)),
                    'numberOfLendingGroups': int(data.get('numberOfLendingGroups', 0)),
                    'numberOfCenterMembers': int(data.get('numberOfCenterMembers', 0)),
                    'attendanceToMeetings': int(data.get('attendanceToMeetings', 0)),
                    'programBenefitsReceived': data.get('programBenefitsReceived', []),
                    'yearsInProgram': int(data.get('yearsInProgram', 0)),
                    'pastdueRatio': int(data.get('pastdueRatio', 0)) if str(data.get('pastdueRatio', '')).isdigit() else 0,
                    'barangayRecord': int(data.get('barangayRecord', 0)) if str(data.get('barangayRecord', '')).isdigit() else 0
                }
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    return update_assessment_data
