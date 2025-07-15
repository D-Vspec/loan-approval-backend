# app.py
from flask import Flask
from flask_migrate import Migrate
from db import db  

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dvdv@localhost/clientdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
migrate = Migrate(app, db)

from client_blueprint import client_bp
app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(debug=True)
