from pymongo import MongoClient
import bcrypt
from datetime import datetime, timezone
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/nirvaha")
db = client.nirvaha
users_collection = db.users

# Test data (adjust as needed)
test_users = [
  {
    "usercode": "A001",
    "username": "admin",
    "email": "admin@company.com",
    "password": "adminSecret1234", 
    "personalInfo": {
        "firstName": "Super",
        "lastName": "Admin",
        "mobile": "+91-9876543200",
        "profilePicture": None
    },
    "role": {
        "roleName": "Admin",
        "department": "Admin",
        "designation": "Admin",
        "permissions": [
            "user.all", "role.all", "customer.all", "loan.all", "report.all"
        ]
    },
    "status": "Active",
    "lastLogin": datetime.now(timezone.utc),
    "createdBy": None,
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
  },
  {
    "usercode": "D002",
    "username": "dev",
    "email": "dev@company.com",
    "password": "devPass!2024", 
    "personalInfo": {
        "firstName": "Dev",
        "lastName": "Technologist",
        "mobile": "+91-9876543201",
        "profilePicture": None
    },
    "role": {
        "roleName": "Developer",
        "department": "IT",
        "designation": "Software Developer",
        "permissions": [
            "report.manage", "system.maintenance", "role.read", "user.read"
        ]
    },
    "status": "Active",
    "lastLogin": datetime.now(timezone.utc),
    "createdBy": None,
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
  },
  {
    "usercode": "O003",
    "username": "ops",
    "email": "ops.@company.com",
    "password": "Ops12345", 
    "personalInfo": {
        "firstName": "Ops",
        "lastName": "Lead",
        "mobile": "+91-9876543202",
        "profilePicture": None
    },
    "role": {
        "roleName": "Operations Lead",
        "department": "Operations",
        "designation": "Team Lead",
        "permissions": [
            "customer.create", "customer.read", "customer.update",
            "loan.approve", "loan.disburse", "report.team", "user.read"
        ]
    },
    "status": "Active",
    "lastLogin": datetime.now(timezone.utc),
    "createdBy": None,
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
  },
  {
    "usercode": "J004",
    "username": "jr.ops",
    "email": "jr.ops@company.com",
    "password": "jrOps!789", 
    "personalInfo": {
        "firstName": "Junior",
        "lastName": "Ops",
        "mobile": "+91-9876543203",
        "profilePicture": None
    },
    "role": {
        "roleName": "Junior Operations",
        "department": "Operations",
        "designation": "Operations Assistant",
        "permissions": [
            "customer.read", "customer.update", "report.team"
        ]
    },
    "status": "Active",
    "lastLogin": datetime.now(timezone.utc),
    "createdBy": None,
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
  },
  {
    "usercode": "B005",
    "username": "banker",
    "email": "banker@company.com",
    "password": "BankerPassword123", 
    "personalInfo": {
        "firstName": "Bank",
        "lastName": "Officer",
        "mobile": "+91-9876543204",
        "profilePicture": None
    },
    "role": {
        "roleName": "Banker",
        "department": "Operations",
        "designation": "Loan Officer",
        "permissions": [
            "customer.create", "customer.read", "customer.update",
            "loan.create", "loan.read", "loan.update", "report.individual"
        ]
    },
    "status": "Active",
    "lastLogin": datetime.now(timezone.utc),
    "createdBy": None,
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
  }
]

users_collection.insert_many(test_users)