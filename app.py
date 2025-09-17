# app.py
from flask import Flask
from flask_migrate import Migrate
from db import db  

from flask_cors import CORS
from flask import request, jsonify

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Dv1234567@localhost/LoanApprovalDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

db.init_app(app)  
migrate = Migrate(app, db)

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

from client_blueprint import client_bp
from auth_blueprint import auth_bp
from assessment_blueprint import assessment_bp
app.register_blueprint(client_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(assessment_bp)

if __name__ == '__main__':
    app.run(debug=True)
