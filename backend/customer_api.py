from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime, timezone
from bson import ObjectId

customer_api = Blueprint('customer_api', __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/nirvaha')
client = MongoClient(MONGO_URI)
db = client.get_default_database()
customers = db['customers']

@customer_api.route('/customer/create', methods=['POST'])
def create_customer():
    data = request.json
    customerCode = data.get('customerCode')
    personalInfo = data.get('personalInfo', {})
    identityDocuments = data.get('identityDocuments', {})
    contactInfo = data.get('contactInfo', {})
    addresses = data.get('addresses', [])
    employment = data.get('employment', [])
    references = data.get('references', [])
    documents = data.get('documents', [])
    kyc = data.get('kyc', {})
    status = data.get('status', 'Active')
    assignedTo = data.get('assignedTo')
    createdBy = data.get('createdBy')
    now = datetime.now(timezone.utc)
    if not customerCode or not personalInfo:
        return jsonify({'success': False, 'message': 'customerCode and personalInfo are required'}), 400
    if customers.find_one({'customerCode': customerCode}):
        return jsonify({'success': False, 'message': 'Customer code already exists'}), 409
    doc = {
        'customerCode': customerCode,
        'personalInfo': personalInfo,
        'identityDocuments': identityDocuments,
        'contactInfo': contactInfo,
        'addresses': addresses,
        'employment': employment,
        'references': references,
        'documents': documents,
        'kyc': kyc,
        'status': status,
        'assignedTo': ObjectId(assignedTo) if assignedTo else None,
        'createdBy': ObjectId(createdBy) if createdBy else None,
        'createdAt': now,
        'updatedAt': now
    }
    customers.insert_one(doc)
    return jsonify({'success': True, 'customerCode': customerCode}), 201

@customer_api.route('/customer/fetch', methods=['GET'])
def fetch_customer():
    customerCode = request.args.get('customerCode')
    mobile = request.args.get('mobile')
    email = request.args.get('email')
    query = {}
    if customerCode:
        query['customerCode'] = customerCode
    if mobile:
        query['contactInfo.mobile.primary'] = mobile
    if email:
        query['contactInfo.email.primary'] = email
    if not query:
        return jsonify({'success': False, 'message': 'At least one filter (customerCode, mobile, or email) is required'}), 400
    results = list(customers.find(query))
    for doc in results:
        doc['_id'] = str(doc['_id'])
        if doc.get('assignedTo'):
            doc['assignedTo'] = str(doc['assignedTo'])
        if doc.get('createdBy'):
            doc['createdBy'] = str(doc['createdBy'])
        # Convert address, employment, references, documents _id fields
        if 'addresses' in doc:
            for a in doc['addresses']:
                if a.get('_id'):
                    a['_id'] = str(a['_id'])
                if a.get('verification', {}).get('verifiedBy'):
                    a['verification']['verifiedBy'] = str(a['verification']['verifiedBy'])
        if 'employment' in doc:
            for e in doc['employment']:
                if e.get('_id'):
                    e['_id'] = str(e['_id'])
                if e.get('verification', {}).get('verifiedBy'):
                    e['verification']['verifiedBy'] = str(e['verification']['verifiedBy'])
        if 'references' in doc:
            for r in doc['references']:
                if r.get('_id'):
                    r['_id'] = str(r['_id'])
        if 'documents' in doc:
            for d in doc['documents']:
                if d.get('_id'):
                    d['_id'] = str(d['_id'])
                if d.get('verification', {}).get('verifiedBy'):
                    d['verification']['verifiedBy'] = str(d['verification']['verifiedBy'])
                if d.get('uploadedBy'):
                    d['uploadedBy'] = str(d['uploadedBy'])
    return jsonify({'success': True, 'results': results}), 200

@customer_api.route('/customer/update', methods=['POST'])
def update_customer():
    data = request.json
    customerCode = data.get('customerCode')
    update_fields = data.get('update_fields', {})
    if not customerCode or not update_fields:
        return jsonify({'success': False, 'message': 'customerCode and update_fields are required'}), 400
    update_fields['updatedAt'] = datetime.now(timezone.utc)
    result = customers.update_one({'customerCode': customerCode}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': 'Customer not found'}), 404
    return jsonify({'success': True, 'message': 'Customer updated successfully'}), 200

@customer_api.route('/customer/delete', methods=['POST'])
def delete_customer():
    data = request.json
    customerCode = data.get('customerCode')
    if not customerCode:
        return jsonify({'success': False, 'message': 'customerCode is required'}), 400
    result = customers.delete_one({'customerCode': customerCode})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'message': 'Customer not found'}), 404
    return jsonify({'success': True, 'message': 'Customer deleted successfully'}), 200 