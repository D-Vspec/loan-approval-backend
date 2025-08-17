from flask import request, jsonify
from werkzeug.security import generate_password_hash

def register_route(db, LoanApprover):
    def register():
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'message': 'No data provided'}), 400
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'message': 'Username and password are required'}), 400
            
            # Check if user already exists
            existing_user = LoanApprover.query.filter_by(username=username).first()
            
            if existing_user:
                return jsonify({'message': 'User already exists'}), 409
            
            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = LoanApprover(
                username=username,
                password=hashed_password
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({
                'message': 'User registered successfully',
                'user_id': new_user.id,
                'username': new_user.username
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Registration failed: {str(e)}'}), 500
    
    return register
