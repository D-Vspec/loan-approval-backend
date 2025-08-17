from flask import Blueprint
from models import LoanApprover
from routes.login import login_route
from routes.register import register_route
from routes.logout import logout_route
from routes.protected_example import protected_route
from db import db
from flask import current_app

auth_bp = Blueprint('auth', __name__)

# Add login route
auth_bp.add_url_rule(
    '/login',
    view_func=lambda: login_route(LoanApprover, current_app)(),
    methods=['GET', 'POST']
)

# Add register route
auth_bp.add_url_rule(
    '/register',
    view_func=register_route(db, LoanApprover),
    methods=['POST']
)

# Add logout route
auth_bp.add_url_rule(
    '/logout',
    view_func=logout_route(),
    methods=['POST']
)

# Add protected route example
auth_bp.add_url_rule(
    '/protected',
    view_func=protected_route(),
    methods=['GET']
)
