from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

loan_api = Blueprint('loan_api', __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loans = db['loans']

@loan_api.route('/loan/create', methods=['POST'])
def create_loan():
    data = request.json
    loanAccountNumber = data.get('loanAccountNumber')
    applicationId = data.get('applicationId')
    customerId = data.get('customerId')
    loanProductId = data.get('loanProductId')
    loanTerms = data.get('loanTerms', {})
    schedule = data.get('schedule', {})
    balances = data.get('balances', {})
    disbursements = data.get('disbursements', [])
    status = data.get('status', {})
    relationshipManagerId = data.get('relationshipManagerId')
    createdBy = data.get('createdBy')
    now = datetime.now(timezone.utc)
    if not loanAccountNumber or not applicationId or not customerId or not loanProductId:
        return jsonify({'success': False, 'message': 'loanAccountNumber, applicationId, customerId, and loanProductId are required'}), 400
    if loans.find_one({'loanAccountNumber': loanAccountNumber}):
        return jsonify({'success': False, 'message': 'Loan account number already exists'}), 409
    doc = {
        'loanAccountNumber': loanAccountNumber,
        'applicationId': ObjectId(applicationId),
        'customerId': ObjectId(customerId),
        'loanProductId': ObjectId(loanProductId),
        'loanTerms': loanTerms,
        'schedule': schedule,
        'balances': balances,
        'disbursements': disbursements,
        'status': status,
        'relationshipManagerId': ObjectId(relationshipManagerId) if relationshipManagerId else None,
        'createdBy': ObjectId(createdBy) if createdBy else None,
        'createdAt': now,
        'updatedAt': now
    }
    loans.insert_one(doc)
    return jsonify({'success': True, 'loanAccountNumber': loanAccountNumber}), 201

@loan_api.route('/loan/fetch', methods=['GET'])
def fetch_loan():
    loanAccountNumber = request.args.get('loanAccountNumber')
    customerId = request.args.get('customerId')
    loanProductId = request.args.get('loanProductId')
    query = {}
    if loanAccountNumber:
        query['loanAccountNumber'] = loanAccountNumber
    if customerId:
        try:
            query['customerId'] = ObjectId(customerId)
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid customerId'}), 400
    if loanProductId:
        try:
            query['loanProductId'] = ObjectId(loanProductId)
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid loanProductId'}), 400
    if not query:
        return jsonify({'success': False, 'message': 'At least one filter (loanAccountNumber, customerId, or loanProductId) is required'}), 400
    results = list(loans.find(query))
    for doc in results:
        doc['_id'] = str(doc['_id'])
        doc['applicationId'] = str(doc['applicationId'])
        doc['customerId'] = str(doc['customerId'])
        doc['loanProductId'] = str(doc['loanProductId'])
        if doc.get('relationshipManagerId'):
            doc['relationshipManagerId'] = str(doc['relationshipManagerId'])
        if doc.get('createdBy'):
            doc['createdBy'] = str(doc['createdBy'])
        # Disbursement _id and verification fields
        if 'disbursements' in doc:
            for d in doc['disbursements']:
                if d.get('_id'):
                    d['_id'] = str(d['_id'])
                if d.get('verification', {}).get('verifiedBy'):
                    d['verification']['verifiedBy'] = str(d['verification']['verifiedBy'])
                if d.get('processedBy'):
                    d['processedBy'] = str(d['processedBy'])
    return jsonify({'success': True, 'results': results}), 200

@loan_api.route('/loan/update', methods=['POST'])
def update_loan():
    data = request.json
    loanAccountNumber = data.get('loanAccountNumber')
    update_fields = data.get('update_fields', {})
    if not loanAccountNumber or not update_fields:
        return jsonify({'success': False, 'message': 'loanAccountNumber and update_fields are required'}), 400
    update_fields['updatedAt'] = datetime.now(timezone.utc)
    result = loans.update_one({'loanAccountNumber': loanAccountNumber}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': 'Loan not found'}), 404
    return jsonify({'success': True, 'message': 'Loan updated successfully'}), 200

@loan_api.route('/loan/delete', methods=['POST'])
def delete_loan():
    data = request.json
    loanAccountNumber = data.get('loanAccountNumber')
    if not loanAccountNumber:
        return jsonify({'success': False, 'message': 'loanAccountNumber is required'}), 400
    result = loans.delete_one({'loanAccountNumber': loanAccountNumber})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'message': 'Loan not found'}), 404
    return jsonify({'success': True, 'message': 'Loan deleted successfully'}), 200 