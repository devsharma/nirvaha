import pytest
from app import app
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loans = db['loans']

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

TEST_LOAN = {
    'loanAccountNumber': 'LA240009999',
    'applicationId': str(ObjectId()),
    'customerId': str(ObjectId()),
    'loanProductId': str(ObjectId()),
    'loanTerms': {
        'principalAmount': 100000,
        'interestRate': 10.5,
        'tenureMonths': 12,
        'monthlyEmi': 8800,
        'processingFee': 1000
    },
    'schedule': {
        'loanStartDate': datetime.now(timezone.utc).isoformat(),
        'firstEmiDate': datetime.now(timezone.utc).isoformat(),
        'lastEmiDate': datetime.now(timezone.utc).isoformat()
    },
    'balances': {
        'outstandingPrincipal': 90000,
        'outstandingInterest': 500,
        'totalOutstanding': 90500,
        'totalPaid': 9500,
        'principalPaid': 8000,
        'interestPaid': 1500,
        'penaltyPaid': 0,
        'overdueAmount': 0,
        'daysPastDue': 0,
        'penaltyAccrued': 0
    },
    'disbursements': [],
    'status': {
        'loanStatus': 'Active',
        'paymentStatus': 'Current',
        'closure': {
            'closureDate': None,
            'closureAmount': None,
            'closureType': None,
            'closureReason': None
        }
    },
    'relationshipManagerId': None,
    'createdBy': None
}

@pytest.fixture(autouse=True)
def cleanup_test_loan():
    loans.delete_many({'loanAccountNumber': TEST_LOAN['loanAccountNumber']})
    yield
    loans.delete_many({'loanAccountNumber': TEST_LOAN['loanAccountNumber']})

def test_create_loan(test_client):
    resp = test_client.post('/loan/create', json=TEST_LOAN)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['loanAccountNumber'] == TEST_LOAN['loanAccountNumber']
    # Check in DB
    loan_doc = loans.find_one({'loanAccountNumber': TEST_LOAN['loanAccountNumber']})
    assert loan_doc is not None
    assert loan_doc['loanTerms']['principalAmount'] == 100000

def test_update_loan(test_client):
    test_client.post('/loan/create', json=TEST_LOAN)
    resp = test_client.post('/loan/update', json={
        'loanAccountNumber': TEST_LOAN['loanAccountNumber'],
        'update_fields': {'loanTerms.interestRate': 11.0, 'status.loanStatus': 'Closed'}
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check update
    loan_doc = loans.find_one({'loanAccountNumber': TEST_LOAN['loanAccountNumber']})
    assert loan_doc['loanTerms']['interestRate'] == 11.0 or loan_doc['status']['loanStatus'] == 'Closed'

def test_fetch_loan_by_loan_account_number(test_client):
    test_client.post('/loan/create', json=TEST_LOAN)
    resp = test_client.get(f"/loan/fetch?loanAccountNumber={TEST_LOAN['loanAccountNumber']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 1
    assert data['results'][0]['loanAccountNumber'] == TEST_LOAN['loanAccountNumber']

def test_fetch_loan_by_customer_id(test_client):
    test_client.post('/loan/create', json=TEST_LOAN)
    resp = test_client.get(f"/loan/fetch?customerId={TEST_LOAN['customerId']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(loan['customerId'] == TEST_LOAN['customerId'] for loan in data['results'])

def test_fetch_loan_by_loan_product_id(test_client):
    test_client.post('/loan/create', json=TEST_LOAN)
    resp = test_client.get(f"/loan/fetch?loanProductId={TEST_LOAN['loanProductId']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(loan['loanProductId'] == TEST_LOAN['loanProductId'] for loan in data['results'])

def test_fetch_loan_no_results(test_client):
    resp = test_client.get("/loan/fetch?loanAccountNumber=DOESNOTEXIST")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 0

def test_delete_loan(test_client):
    test_client.post('/loan/create', json=TEST_LOAN)
    resp = test_client.post('/loan/delete', json={
        'loanAccountNumber': TEST_LOAN['loanAccountNumber']
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check delete
    loan_doc = loans.find_one({'loanAccountNumber': TEST_LOAN['loanAccountNumber']})
    assert loan_doc is None 