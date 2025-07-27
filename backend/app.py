from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from pymongo import MongoClient
import random
import string

from loan_product_api import loan_product_api
from loan_application_api import loan_application_api
from loan_api import loan_api
from customer_api import customer_api
from user_api import user_api

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_collection = db['users']


app.register_blueprint(loan_product_api)
app.register_blueprint(loan_application_api)
app.register_blueprint(loan_api)
app.register_blueprint(customer_api)
app.register_blueprint(user_api)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Password check: bcrypt
    if password != user['password']:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Prepare user details to return (excluding sensitive info)
    user_details = {
        'username': user.get('username'),
        'email': user.get('email'),
        'role': user.get('role'),
        'status': user.get('status'),
        'personalInfo': user.get('personalInfo', {}),
        'usercode': user.get('usercode'),
        'lastLogin': user.get('lastLogin'),
        'createdAt': user.get('createdAt'),
        'updatedAt': user.get('updatedAt')
    }

    # Optionally update lastLogin
    from datetime import datetime, timezone
    users_collection.update_one({'username': username}, {'$set': {'lastLogin': datetime.now(timezone.utc)}})

    return jsonify({'success': True, 'message': 'Login successful', 'user': user_details}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050) 