from flask import jsonify
from routes.auth_middleware import token_required

def protected_route():
    @token_required
    def get_protected_data(current_user_id, current_username):
        return jsonify({
            'message': 'This is protected data',
            'user_id': current_user_id,
            'username': current_username,
            'data': 'Only authenticated users can see this'
        }), 200
    
    return get_protected_data
