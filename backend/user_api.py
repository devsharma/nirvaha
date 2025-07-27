from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
import random
import string
import bcrypt
from datetime import datetime
from datetime import timezone
from bson import ObjectId

user_api = Blueprint('user_api', __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_collection = db['users']

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@user_api.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    personalInfo = data.get('personalInfo', {})
    role = data.get('role', {})
    status = data.get('status', 'Active')
    createdBy = data.get('createdBy')
    if not username or not password or not email or not role:
        return jsonify({'success': False, 'message': 'username, password, email, and role are required'}), 400
    if users_collection.find_one({'username': username}):
        return jsonify({'success': False, 'message': 'Username already exists'}), 409
    # Generate usercode: user<random 3 digits>
    def generate_usercode():
        return f"user{''.join(random.choices(string.digits, k=3))}"
    usercode = generate_usercode()
    # This code checks if the generated usercode already exists in the users collection.
    # If it does, it generates a new usercode and checks again, repeating until a unique usercode is found.
    while users_collection.find_one({'usercode': usercode}):
        usercode = generate_usercode()
    # now = datetime.utcnow()
    now = datetime.now(timezone.utc)
    user_doc = {
        'usercode': usercode,
        'username': username,
        'email': email,
        'password': hash_password(password),
        'personalInfo': personalInfo,
        'role': role,
        'status': status,
        'lastLogin': None,
        'createdBy': ObjectId(createdBy) if createdBy else None,
        'createdAt': now,
        'updatedAt': now
    }
    users_collection.insert_one(user_doc)
    return jsonify({'success': True, 'usercode': usercode}), 201

@user_api.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not username or not old_password or not new_password:
        return jsonify({'success': False, 'message': 'username, old_password, and new_password are required'}), 400
    user = users_collection.find_one({'username': username})
    if not user or not check_password(old_password, user['password']):
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    users_collection.update_one({'username': username}, {'$set': {'password': hash_password(new_password), 'updatedAt': datetime.now(timezone.utc)}})
    return jsonify({'success': True, 'message': 'Password updated successfully'}), 200

@user_api.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    username = data.get('username')
    update_fields = data.get('update_fields', {})
    if not username or not update_fields:
        return jsonify({'success': False, 'message': 'username and update_fields are required'}), 400
    # If updating password, hash it
    if 'password' in update_fields:
        update_fields['password'] = hash_password(update_fields['password'])
    update_fields['updatedAt'] = datetime.now(timezone.utc)
    result = users_collection.update_one({'username': username}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return jsonify({'success': True, 'message': 'User details updated successfully'}), 200

@user_api.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'username is required'}), 400
    result = users_collection.delete_one({'username': username})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return jsonify({'success': True, 'message': 'User deleted successfully'}), 200 
    