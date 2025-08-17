from flask import request, jsonify, make_response, redirect, url_for
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta, timezone

def login_route(LoanApprover, app):
    def login():
        if request.method == 'POST':
            # Handle both JSON and form data
            if request.is_json:
                username = request.json.get('username')
                password = request.json.get('password')
            else:
                username = request.form.get('username')
                password = request.form.get('password')
            
            if not username or not password:
                return jsonify({'message': 'Username and password are required'}), 400
            
            # Query by username
            user = LoanApprover.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                return jsonify({'message': 'Invalid username or password'}), 401

            # Generate JWT token
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            # Return JSON response with token
            if request.is_json:
                return jsonify({
                    'message': 'Login successful',
                    'token': token,
                    'user_id': user.id,
                    'username': user.username
                }), 200
            else:
                # For form-based login, redirect with cookie
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('jwt_token', token)
                return response
        
        # Handle GET request (login form)
        return jsonify({'message': 'Login endpoint. Send POST request with username and password.'}), 200
    
    return login
