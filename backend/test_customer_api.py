import pytest
from app import app
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
customers = db['customers']

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

TEST_CUSTOMER = {
    'customerCode': 'CUSTTEST001',
    'personalInfo': {
        'firstName': 'Test',
        'middleName': 'Middle',
        'lastName': 'User',
        'dateOfBirth': datetime(1990, 1, 1, tzinfo=timezone.utc).isoformat(),
        'gender': 'Male',
        'maritalStatus': 'Single',
        'nationality': 'Indian'
    },
    'identityDocuments': {
        'panNumber': 'ABCDE1234F',
        'aadharNumber': '123456789012',
        'voterId': 'ABC1234567',
        'drivingLicense': 'MH12345678',
        'passportNumber': None
    },
    'contactInfo': {
        'mobile': {'primary': '+91-9999999999', 'secondary': None},
        'email': {'primary': 'test.user@email.com', 'secondary': None}
    },
    'addresses': [],
    'employment': [],
    'references': [],
    'documents': [],
    'kyc': {'status': 'Pending'},
    'status': 'Active',
    'assignedTo': None,
    'createdBy': None
}

@pytest.fixture(autouse=True)
def cleanup_test_customer():
    customers.delete_many({'customerCode': TEST_CUSTOMER['customerCode']})
    yield
    customers.delete_many({'customerCode': TEST_CUSTOMER['customerCode']})

def test_create_customer(test_client):
    resp = test_client.post('/customer/create', json=TEST_CUSTOMER)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['customerCode'] == TEST_CUSTOMER['customerCode']
    # Check in DB
    cust_doc = customers.find_one({'customerCode': TEST_CUSTOMER['customerCode']})
    assert cust_doc is not None
    assert cust_doc['personalInfo']['firstName'] == 'Test'

def test_fetch_customer_by_code(test_client):
    test_client.post('/customer/create', json=TEST_CUSTOMER)
    resp = test_client.get(f"/customer/fetch?customerCode={TEST_CUSTOMER['customerCode']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 1
    assert data['results'][0]['customerCode'] == TEST_CUSTOMER['customerCode']

# def test_fetch_customer_by_mobile(test_client):
#     test_client.post('/customer/create', json=TEST_CUSTOMER)
#     resp = test_client.get(f"/customer/fetch?mobile={TEST_CUSTOMER['contactInfo']['mobile']['primary']}")
#     data = resp.get_json()
#     assert resp.status_code == 200
#     assert data['success'] is True
#     assert any(cust['contactInfo']['mobile']['primary'] == TEST_CUSTOMER['contactInfo']['mobile']['primary'] for cust in data['results'])

def test_fetch_customer_by_email(test_client):
    test_client.post('/customer/create', json=TEST_CUSTOMER)
    resp = test_client.get(f"/customer/fetch?email={TEST_CUSTOMER['contactInfo']['email']['primary']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(cust['contactInfo']['email']['primary'] == TEST_CUSTOMER['contactInfo']['email']['primary'] for cust in data['results'])

def test_update_customer(test_client):
    test_client.post('/customer/create', json=TEST_CUSTOMER)
    resp = test_client.post('/customer/update', json={
        'customerCode': TEST_CUSTOMER['customerCode'],
        'update_fields': {'status': 'Inactive'}
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check update
    cust_doc = customers.find_one({'customerCode': TEST_CUSTOMER['customerCode']})
    assert cust_doc['status'] == 'Inactive'

def test_delete_customer(test_client):
    test_client.post('/customer/create', json=TEST_CUSTOMER)
    resp = test_client.post('/customer/delete', json={
        'customerCode': TEST_CUSTOMER['customerCode']
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check delete
    cust_doc = customers.find_one({'customerCode': TEST_CUSTOMER['customerCode']})
    assert cust_doc is None 