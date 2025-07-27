import pytest
from app import app
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loan_applications = db['loanapplications']

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

TEST_APPLICATION = {
    'applicationNumber': 'LA2024009999',
    'customerId': str(ObjectId()),
    'loanProductId': str(ObjectId()),
    'applicationDetails': {
        'requestedAmount': 100000,
        'requestedTenure': 24,
        'purposeOfLoan': 'Test Loan',
        'loanType': 'Personal'
    },
    'assessment': {
        'assessedAmount': 95000,
        'approvedAmount': 90000,
        'approvedTenure': 24,
        'approvedRate': 11.5,
        'monthlyEmi': 4200,
        'processingFee': 1500,
        'creditScore': 700,
        'incomeAssessment': {
            'declaredIncome': 50000,
            'assessedIncome': 48000,
            'otherObligations': 5000,
            'availableIncome': 43000
        }
    },
    'workflow': {
        'currentStage': 'Data Entry',
        'status': 'Draft',
        'stageHistory': []
    },
    'decision': {
        'finalDecision': 'Draft',
        'decisionDate': None,
        'decisionBy': None,
        'decisionNotes': '',
        'conditions': [],
        'rejectionReason': None
    },
    'submittedDate': datetime.now(timezone.utc).isoformat(),
    'createdBy': None
}

@pytest.fixture(autouse=True)
def cleanup_test_application():
    loan_applications.delete_many({'applicationNumber': TEST_APPLICATION['applicationNumber']})
    yield
    loan_applications.delete_many({'applicationNumber': TEST_APPLICATION['applicationNumber']})

def test_create_loan_application(test_client):
    resp = test_client.post('/loan_application/create', json=TEST_APPLICATION)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['applicationNumber'] == TEST_APPLICATION['applicationNumber']
    # Check in DB
    app_doc = loan_applications.find_one({'applicationNumber': TEST_APPLICATION['applicationNumber']})
    assert app_doc is not None
    assert app_doc['applicationDetails']['purposeOfLoan'] == 'Test Loan'

def test_update_loan_application(test_client):
    test_client.post('/loan_application/create', json=TEST_APPLICATION)
    resp = test_client.post('/loan_application/update', json={
        'applicationNumber': TEST_APPLICATION['applicationNumber'],
        'update_fields': {'workflow.status': 'Submitted', 'assessment.approvedAmount': 85000}
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check update
    app_doc = loan_applications.find_one({'applicationNumber': TEST_APPLICATION['applicationNumber']})
    assert app_doc['workflow']['status'] == 'Submitted' or app_doc['assessment']['approvedAmount'] == 85000

def test_delete_loan_application(test_client):
    test_client.post('/loan_application/create', json=TEST_APPLICATION)
    resp = test_client.post('/loan_application/delete', json={
        'applicationNumber': TEST_APPLICATION['applicationNumber']
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check delete
    app_doc = loan_applications.find_one({'applicationNumber': TEST_APPLICATION['applicationNumber']})
    assert app_doc is None

def test_fetch_loan_application_by_application_number(test_client):
    test_client.post('/loan_application/create', json=TEST_APPLICATION)
    resp = test_client.get(f"/loan_application/fetch?applicationNumber={TEST_APPLICATION['applicationNumber']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 1
    assert data['results'][0]['applicationNumber'] == TEST_APPLICATION['applicationNumber']

def test_fetch_loan_application_by_customer_id(test_client):
    test_client.post('/loan_application/create', json=TEST_APPLICATION)
    resp = test_client.get(f"/loan_application/fetch?customerId={TEST_APPLICATION['customerId']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(app['customerId'] == TEST_APPLICATION['customerId'] for app in data['results'])

def test_fetch_loan_application_by_loan_product_id(test_client):
    test_client.post('/loan_application/create', json=TEST_APPLICATION)
    resp = test_client.get(f"/loan_application/fetch?loanProductId={TEST_APPLICATION['loanProductId']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(app['loanProductId'] == TEST_APPLICATION['loanProductId'] for app in data['results'])

def test_fetch_loan_application_no_results(test_client):
    resp = test_client.get("/loan_application/fetch?applicationNumber=DOESNOTEXIST")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 0 