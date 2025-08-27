from flask import Blueprint
from models import (
    Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense,
    PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis, Residency,
    FamilyAndToiletStatus
)
from db import db
from routes.get_client_details import get_client_details_route
from routes.get_all_clients import get_all_clients_route
from routes.check_client_verification import check_client_verification_route
from routes.verify_client import verify_client_route
from routes.reject_client import reject_client_route
from routes.update_client_data import update_client_data_route


client_bp = Blueprint('client', __name__)

client_bp.add_url_rule(
    '/client/<int:client_id>',
    view_func=get_client_details_route(
        Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense,
        PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis, Residency, FamilyAndToiletStatus
    ),
    methods=['GET']
)
client_bp.add_url_rule(
    '/clients',
    view_func=get_all_clients_route(Client),
    methods=['GET']
)

client_bp.add_url_rule(
    '/client/<int:client_id>/verification-status',
    view_func=check_client_verification_route(Client, FamilyAndToiletStatus),
    methods=['GET']
)

client_bp.add_url_rule(
    '/client/<int:client_id>/verify',
    view_func=verify_client_route(db, Client),
    methods=['PUT', 'POST', 'OPTIONS']
)

client_bp.add_url_rule(
    '/client/<int:client_id>/reject',
    view_func=reject_client_route(db, Client),
    methods=['PUT', 'POST', 'OPTIONS']
)

client_bp.add_url_rule(
    '/client/<int:client_id>/update',
    view_func=update_client_data_route(db, Client, AddressInformation, Beneficiaries, CoInsured, Income, Expense, PrimaryRepaymentSource, OtherRepaymentSource, Residency, FamilyAndToiletStatus),
    methods=['PUT', 'PATCH', 'OPTIONS']
)


# Utility functions are now in routes/utils.py