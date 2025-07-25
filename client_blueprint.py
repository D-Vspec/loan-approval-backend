from flask import Blueprint
from models import (
    Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense,
    PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis, Residency,
    FamilyAndToiletStatus, TimeInProgram, CenterCollectionRecord, PaymentHistory,
    LendingGroups, CenterStatusMembers, MeetingAttendance, ProgramBenefitsReceived,
    YearsInProgram, PastdueRatio
)
from db import db
from routes.process_form_data import process_form_data_route
from routes.get_client_details import get_client_details_route
from routes.get_all_clients import get_all_clients_route
from routes.process_assessment_data import process_assessment_data_route

client_bp = Blueprint('client', __name__)

client_bp.add_url_rule(
    '/process_form_data',
    view_func=process_form_data_route(db, Client, AddressInformation, Beneficiaries, CoInsured, PrimaryRepaymentSource, OtherRepaymentSource),
    methods=['POST', 'OPTIONS']
)
client_bp.add_url_rule(
    '/client/<int:client_id>',
    view_func=get_client_details_route(
        Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense,
        PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis, Residency,
        FamilyAndToiletStatus, TimeInProgram, CenterCollectionRecord, PaymentHistory,
        LendingGroups, CenterStatusMembers, MeetingAttendance, ProgramBenefitsReceived,
        YearsInProgram, PastdueRatio
    ),
    methods=['GET']
)
client_bp.add_url_rule(
    '/clients',
    view_func=get_all_clients_route(Client),
    methods=['GET']
)

client_bp.add_url_rule(
    '/process_assessment_data',
    view_func=process_assessment_data_route(
        db, Client, TimeInProgram, CenterCollectionRecord, PaymentHistory,
        LendingGroups, CenterStatusMembers, MeetingAttendance, 
        ProgramBenefitsReceived, YearsInProgram, PastdueRatio
    ),
    methods=['POST', 'OPTIONS']
)


# Utility functions are now in routes/utils.py