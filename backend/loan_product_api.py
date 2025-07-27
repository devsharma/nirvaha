from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

loan_product_api = Blueprint('loan_product_api', __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loan_products = db['loanproducts']

@loan_product_api.route('/loan_product/create', methods=['POST'])
def create_loan_product():
    data = request.json
    productCode = data.get('productCode')
    productName = data.get('productName')
    category = data.get('category')
    description = data.get('description')
    loanTerms = data.get('loanTerms', {})
    interestRates = data.get('interestRates', {})
    fees = data.get('fees', {})
    isActive = data.get('isActive', True)
    effectiveFrom = data.get('effectiveFrom')
    effectiveTo = data.get('effectiveTo')
    createdBy = data.get('createdBy')
    now = datetime.now(timezone.utc)
    if not productCode or not productName or not category:
        return jsonify({'success': False, 'message': 'productCode, productName, and category are required'}), 400
    if loan_products.find_one({'productCode': productCode}):
        return jsonify({'success': False, 'message': 'Product code already exists'}), 409
    doc = {
        'productCode': productCode,
        'productName': productName,
        'category': category,
        'description': description,
        'loanTerms': loanTerms,
        'interestRates': interestRates,
        'fees': fees,
        'isActive': isActive,
        'effectiveFrom': datetime.fromisoformat(effectiveFrom) if effectiveFrom else now,
        'effectiveTo': datetime.fromisoformat(effectiveTo) if effectiveTo else None,
        'createdBy': ObjectId(createdBy) if createdBy else None,
        'createdAt': now,
        'updatedAt': now
    }
    loan_products.insert_one(doc)
    return jsonify({'success': True, 'productCode': productCode}), 201

@loan_product_api.route('/loan_product/update', methods=['POST'])
def update_loan_product():
    data = request.json
    productCode = data.get('productCode')
    update_fields = data.get('update_fields', {})
    if not productCode or not update_fields:
        return jsonify({'success': False, 'message': 'productCode and update_fields are required'}), 400
    update_fields['updatedAt'] = datetime.now(timezone.utc)
    result = loan_products.update_one({'productCode': productCode}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': 'Loan product not found'}), 404
    return jsonify({'success': True, 'message': 'Loan product updated successfully'}), 200

@loan_product_api.route('/loan_product/delete', methods=['POST'])
def delete_loan_product():
    data = request.json
    productCode = data.get('productCode')
    if not productCode:
        return jsonify({'success': False, 'message': 'productCode is required'}), 400
    result = loan_products.delete_one({'productCode': productCode})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'message': 'Loan product not found'}), 404
    return jsonify({'success': True, 'message': 'Loan product deleted successfully'}), 200

@loan_product_api.route('/loan_product/fetch', methods=['GET'])
def fetch_loan_product():
    productCode = request.args.get('productCode')
    productName = request.args.get('productName')
    query = {}
    if productCode:
        query['productCode'] = productCode
    if productName:
        query['productName'] = productName
    if not query:
        return jsonify({'success': False, 'message': 'At least one filter (productCode or productName) is required'}), 400
    results = list(loan_products.find(query))
    for doc in results:
        doc['_id'] = str(doc['_id'])
        if doc.get('createdBy'):
            doc['createdBy'] = str(doc['createdBy'])
    return jsonify({'success': True, 'results': results}), 200 