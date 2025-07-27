import pytest
from app import app
from pymongo import MongoClient
import os
from datetime import datetime, timezone

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loan_products = db['loanproducts']

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

TEST_PRODUCT = {
    'productCode': 'TESTPL001',
    'productName': 'Test Personal Loan',
    'category': 'Personal',
    'description': 'Test loan product',
    'loanTerms': {
        'amount': {'min': 10000, 'max': 50000},
        'tenure': {'minMonths': 6, 'maxMonths': 24}
    },
    'interestRates': {
        'baseRate': 10.0, 'minRate': 8.0, 'maxRate': 12.0, 'rateType': 'Fixed'
    },
    'fees': {
        'processing': {'percentage': 1.0, 'fixedAmount': 0, 'minAmount': 500, 'maxAmount': 2000},
        'prepaymentPenalty': 1.0, 'latePaymentCharges': 1.0, 'bounceCharges': 200
    },
    'isActive': True,
    'effectiveFrom': datetime.now(timezone.utc).isoformat(),
    'effectiveTo': None,
    'createdBy': None
}

@pytest.fixture(autouse=True)
def cleanup_test_product():
    loan_products.delete_many({'productCode': TEST_PRODUCT['productCode']})
    yield
    loan_products.delete_many({'productCode': TEST_PRODUCT['productCode']})

def test_create_loan_product(test_client):
    resp = test_client.post('/loan_product/create', json=TEST_PRODUCT)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['productCode'] == TEST_PRODUCT['productCode']
    # Check in DB
    product = loan_products.find_one({'productCode': TEST_PRODUCT['productCode']})
    assert product is not None
    assert product['productName'] == TEST_PRODUCT['productName']

def test_update_loan_product(test_client):
    test_client.post('/loan_product/create', json=TEST_PRODUCT)
    resp = test_client.post('/loan_product/update', json={
        'productCode': TEST_PRODUCT['productCode'],
        'update_fields': {'productName': 'Updated Loan Name', 'isActive': False}
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check update
    product = loan_products.find_one({'productCode': TEST_PRODUCT['productCode']})
    assert product['productName'] == 'Updated Loan Name'
    assert product['isActive'] is False

def test_delete_loan_product(test_client):
    test_client.post('/loan_product/create', json=TEST_PRODUCT)
    resp = test_client.post('/loan_product/delete', json={
        'productCode': TEST_PRODUCT['productCode']
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # Check delete
    product = loan_products.find_one({'productCode': TEST_PRODUCT['productCode']})
    assert product is None

def test_fetch_loan_product_by_product_code(test_client):
    test_client.post('/loan_product/create', json=TEST_PRODUCT)
    resp = test_client.get(f"/loan_product/fetch?productCode={TEST_PRODUCT['productCode']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 1
    assert data['results'][0]['productCode'] == TEST_PRODUCT['productCode']

def test_fetch_loan_product_by_product_name(test_client):
    test_client.post('/loan_product/create', json=TEST_PRODUCT)
    resp = test_client.get(f"/loan_product/fetch?productName={TEST_PRODUCT['productName']}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert any(prod['productName'] == TEST_PRODUCT['productName'] for prod in data['results'])

def test_fetch_loan_product_no_results(test_client):
    resp = test_client.get("/loan_product/fetch?productCode=DOESNOTEXIST")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert len(data['results']) == 0 