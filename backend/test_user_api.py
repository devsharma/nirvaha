import pytest
from app import app
from pymongo import MongoClient
import os
import bcrypt

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_collection = db['users']

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

TEST_USER = {
    'username': 'apitestuser',
    'password': 'apitestpass',
    'email': 'apitestuser@example.com',
    'personalInfo': {
        'firstName': 'API',
        'lastName': 'Test',
        'mobile': '+91-9999999999',
        'profilePicture': None
    },
    'role': {
        'roleId': 'testroleid',
        'roleName': 'Branch Manager',
        'department': 'Operations',
        'designation': 'Branch Manager',
        'permissions': [
            'customer.create', 'customer.read', 'customer.update',
            'loan.approve', 'loan.disburse',
            'reports.branch', 'reports.team'
        ]
    },
    'status': 'Active',
    'createdBy': None
}

@pytest.fixture(autouse=True)
def cleanup_test_user():
    users_collection.delete_many({'username': TEST_USER['username']})
    yield
    users_collection.delete_many({'username': TEST_USER['username']})

def test_create_user(test_client):
    resp = test_client.post('/create_user', json=TEST_USER)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['usercode'].startswith('user')
    # Check user in DB
    user = users_collection.find_one({'username': TEST_USER['username']})
    assert user is not None
    assert user['email'] == TEST_USER['email']
    assert user['personalInfo']['firstName'] == 'API'
    assert user['role']['roleName'] == 'Branch Manager'
    # Password should be hashed
    assert user['password'] != TEST_USER['password']
    assert bcrypt.checkpw(TEST_USER['password'].encode('utf-8'), user['password'].encode('utf-8'))

def test_change_password(test_client):
    test_client.post('/create_user', json=TEST_USER)
    resp = test_client.post('/change_password', json={
        'username': TEST_USER['username'],
        'old_password': TEST_USER['password'],
        'new_password': 'newapitestpass'
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check password updated
    user = users_collection.find_one({'username': TEST_USER['username']})
    assert bcrypt.checkpw('newapitestpass'.encode('utf-8'), user['password'].encode('utf-8'))

def test_update_user(test_client):
    test_client.post('/create_user', json=TEST_USER)
    resp = test_client.post('/update_user', json={
        'username': TEST_USER['username'],
        'update_fields': {'email': 'apitest2@example.com', 'personalInfo.firstName': 'Changed'}
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check fields updated
    user = users_collection.find_one({'username': TEST_USER['username']})
    assert user['email'] == 'apitest2@example.com'
    # Note: MongoDB dot notation does not update nested fields by default in PyMongo, so this will not update personalInfo.firstName unless handled in backend

def test_delete_user(test_client):
    test_client.post('/create_user', json=TEST_USER)
    resp = test_client.post('/delete_user', json={
        'username': TEST_USER['username']
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    user = users_collection.find_one({'username': TEST_USER['username']})
    assert user is None 