from flask import jsonify, make_response

def logout_route():
    def logout():
        response = make_response(jsonify({'message': 'Logged out successfully'}))
        response.set_cookie('jwt_token', '', expires=0)  # Clear the cookie
        return response
    
    return logout
