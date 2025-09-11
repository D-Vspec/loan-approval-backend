from flask import request, jsonify
from datetime import datetime

def process_assessment_data_route(db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory, 
                                 LendingGroups, CenterStatusMembers, MeetingAttendance, 
                                 ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord):
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
                PastdueRatio.query.filter_by(client_id=client_id).all(),
                BarangayRecord.query.filter_by(client_id=client_id).all()
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
                numeric_to_name = {
                    '1': 'SpouseOnlyKnown',
                    '2': 'BornAndNoRecord',
                    '3': 'ReputableFamily',
                    '4': 'RelativeInCouncil',
                    '5': 'FamilyElected'
                }
                slug_to_name = {
                    'spouse_only_known': 'SpouseOnlyKnown',
                    'born_and_no_record': 'BornAndNoRecord',
                    'reputable_family': 'ReputableFamily',
                    'relative_in_council': 'RelativeInCouncil',
                    'family_elected': 'FamilyElected'
                }
                s = str(value)
                if s in numeric_to_name:
                    return numeric_to_name[s]
                if s in slug_to_name:
                    return slug_to_name[s]
                # Allow direct enum key passthrough if already CamelCase
                if s in numeric_to_name.values():
                    return s
                return 'SpouseOnlyKnown'

            def barangay_record_score(value):
                numeric_score = {
                    'SpouseOnlyKnown': 1,
                    'BornAndNoRecord': 2,
                    'ReputableFamily': 3,
                    'RelativeInCouncil': 4,
                    'FamilyElected': 5
                }
                s = str(value)
                if s.isdigit():
                    try:
                        i = int(s)
                        return i if 1 <= i <= 5 else 0
                    except Exception:
                        return 0
                # map slug/camel to name then score
                name = map_barangay_record(s)
                return numeric_score.get(name, 0)

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
            if data.get('programBenefitsReceived') and isinstance(data['programBenefitsReceived'], list):
                for benefit_name in data['programBenefitsReceived']:
                    mapped_benefit = map_program_benefits(benefit_name)
                    if mapped_benefit:
                        program_benefit = ProgramBenefitsReceived(client_id=client_id, benefits_name=mapped_benefit)
                        db.session.add(program_benefit)
            
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
            
            # Barangay Record
            if data.get('barangayRecord'):
                barangay_record = BarangayRecord()
                barangay_record.client_id = client_id
                mapped = map_barangay_record(data['barangayRecord'])
                barangay_record.record_status = mapped
                barangay_record.score = barangay_record_score(data['barangayRecord'])
                db.session.add(barangay_record)
            
            # Commit all changes
            db.session.commit()
            
            # Calculate total score
            total_score = 0
            for field in ['timeInProgram', 'centerCollectionRecord', 'paymentHistory', 
                         'numberOfLendingGroups', 'numberOfCenterMembers', 'attendanceToMeetings',
                         'yearsInProgram', 'pastdueRatio', 'barangayRecord']:
                if field == 'barangayRecord':
                    total_score += barangay_record_score(data.get('barangayRecord')) if data.get('barangayRecord') else 0
                elif data.get(field) and str(data[field]).isdigit():
                    total_score += int(data[field])
            
            return jsonify({
                'message': 'Assessment data processed successfully',
                'client_id': client_id,
                'assessment_date': data.get('assessmentDate'),
                'remarks': data.get('remarks'),
                'total_score': total_score,
                'individual_scores': {
                    'timeInProgram': int(data.get('timeInProgram', 0)) if str(data.get('timeInProgram', '')).isdigit() else 0,
                    'centerCollectionRecord': int(data.get('centerCollectionRecord', 0)) if str(data.get('centerCollectionRecord', '')).isdigit() else 0,
                    'paymentHistory': int(data.get('paymentHistory', 0)) if str(data.get('paymentHistory', '')).isdigit() else 0,
                    'numberOfLendingGroups': int(data.get('numberOfLendingGroups', 0)) if str(data.get('numberOfLendingGroups', '')).isdigit() else 0,
                    'numberOfCenterMembers': int(data.get('numberOfCenterMembers', 0)) if str(data.get('numberOfCenterMembers', '')).isdigit() else 0,
                    'attendanceToMeetings': int(data.get('attendanceToMeetings', 0)) if str(data.get('attendanceToMeetings', '')).isdigit() else 0,
                    'programBenefitsReceived': data.get('programBenefitsReceived', []),
                    'yearsInProgram': int(data.get('yearsInProgram', 0)) if str(data.get('yearsInProgram', '')).isdigit() else 0,
                    'pastdueRatio': int(data.get('pastdueRatio', 0)) if str(data.get('pastdueRatio', '')).isdigit() else 0,
                    'barangayRecord': barangay_record_score(data.get('barangayRecord')) if data.get('barangayRecord') else 0
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    return process_assessment_data
