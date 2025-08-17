from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token format invalid'}), 401
        
        # Check for token in cookies
        elif 'jwt_token' in request.cookies:
            token = request.cookies.get('jwt_token')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
            current_username = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, current_username, *args, **kwargs)
    
    return decorated

def get_current_user():
    """Helper function to get current user from token"""
    token = None
    
    # Check for token in headers
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]  # Bearer <token>
        except IndexError:
            return None
    
    # Check for token in cookies
    elif 'jwt_token' in request.cookies:
        token = request.cookies.get('jwt_token')
    
    if not token:
        return None
    
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return {
            'user_id': data['user_id'],
            'username': data['username']
        }
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
