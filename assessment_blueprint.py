# assessment_blueprint.py
from flask import Blueprint
from db import db
from models.client import Client
from models.assessment import TimeInProgram, CenterCollectionRecord, PaymentHistory, LendingGroups, CenterStatusMembers, MeetingAttendance, ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord
from routes.process_assessment_data import process_assessment_data_route
from routes.update_assessment_data import update_assessment_data_route
from routes.get_assessment_data import get_assessment_data_route

assessment_bp = Blueprint('assessment_bp', __name__)

# Pass the db and model instances to the route function
process_assessment_data = process_assessment_data_route(db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory, 
                                                         LendingGroups, CenterStatusMembers, MeetingAttendance, 
                                                         ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord)

update_assessment_data = update_assessment_data_route(db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory,
                                                       LendingGroups, CenterStatusMembers, MeetingAttendance,
                                                       ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord)

get_assessment_data = get_assessment_data_route(Client, TimeInProgram, CenterCollectionRecord, PaymentHistory,
                                                 LendingGroups, CenterStatusMembers, MeetingAttendance,
                                                 ProgramBenefitsReceived, YearsInProgram, PastdueRatio, BarangayRecord)


assessment_bp.route('/process_assessment_data', methods=['POST'])(process_assessment_data)
assessment_bp.route('/assessment/<int:client_id>', methods=['PUT'])(update_assessment_data)
assessment_bp.route('/client/<int:client_id>/assessment', methods=['GET'])(get_assessment_data)
