from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

loan_application_api = Blueprint('loan_application_api', __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
loan_applications = db['loanapplications']

@loan_application_api.route('/loan_application/create', methods=['POST'])
def create_loan_application():
    data = request.json
    applicationNumber = data.get('applicationNumber')
    customerId = data.get('customerId')
    loanProductId = data.get('loanProductId')
    applicationDetails = data.get('applicationDetails', {})
    assessment = data.get('assessment', {})
    workflow = data.get('workflow', {})
    decision = data.get('decision', {})
    submittedDate = data.get('submittedDate')
    createdBy = data.get('createdBy')
    now = datetime.now(timezone.utc)
    if not applicationNumber or not customerId or not loanProductId:
        return jsonify({'success': False, 'message': 'applicationNumber, customerId, and loanProductId are required'}), 400
    if loan_applications.find_one({'applicationNumber': applicationNumber}):
        return jsonify({'success': False, 'message': 'Application number already exists'}), 409
    doc = {
        'applicationNumber': applicationNumber,
        'customerId': ObjectId(customerId),
        'loanProductId': ObjectId(loanProductId),
        'applicationDetails': applicationDetails,
        'assessment': assessment,
        'workflow': workflow,
        'decision': decision,
        'submittedDate': datetime.fromisoformat(submittedDate) if submittedDate else now,
        'createdBy': ObjectId(createdBy) if createdBy else None,
        'createdAt': now,
        'updatedAt': now
    }
    loan_applications.insert_one(doc)
    return jsonify({'success': True, 'applicationNumber': applicationNumber}), 201

@loan_application_api.route('/loan_application/update', methods=['POST'])
def update_loan_application():
    data = request.json
    applicationNumber = data.get('applicationNumber')
    update_fields = data.get('update_fields', {})
    if not applicationNumber or not update_fields:
        return jsonify({'success': False, 'message': 'applicationNumber and update_fields are required'}), 400
    update_fields['updatedAt'] = datetime.now(timezone.utc)
    result = loan_applications.update_one({'applicationNumber': applicationNumber}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': 'Loan application not found'}), 404
    return jsonify({'success': True, 'message': 'Loan application updated successfully'}), 200

@loan_application_api.route('/loan_application/delete', methods=['POST'])
def delete_loan_application():
    data = request.json
    applicationNumber = data.get('applicationNumber')
    if not applicationNumber:
        return jsonify({'success': False, 'message': 'applicationNumber is required'}), 400
    result = loan_applications.delete_one({'applicationNumber': applicationNumber})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'message': 'Loan application not found'}), 404
    return jsonify({'success': True, 'message': 'Loan application deleted successfully'}), 200

@loan_application_api.route('/loan_application/fetch', methods=['GET'])
def fetch_loan_application():
    applicationNumber = request.args.get('applicationNumber')
    customerId = request.args.get('customerId')
    loanProductId = request.args.get('loanProductId')
    query = {}
    if applicationNumber:
        query['applicationNumber'] = applicationNumber
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
        return jsonify({'success': False, 'message': 'At least one filter (applicationNumber, customerId, or loanProductId) is required'}), 400
    results = list(loan_applications.find(query))
    for doc in results:
        doc['_id'] = str(doc['_id'])
        doc['customerId'] = str(doc['customerId'])
        doc['loanProductId'] = str(doc['loanProductId'])
        if doc.get('createdBy'):
            doc['createdBy'] = str(doc['createdBy'])
    return jsonify({'success': True, 'results': results}), 200 