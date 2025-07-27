from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

# Replace this with your actual MongoDB URI
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/nirvaha")

mongo = PyMongo(app)
users_collection = mongo.db.users

def get_all_users():
    users = list(users_collection.find({}))
    for user in users:
        # Remove sensitive data (password) before printing
        user.pop('passwordHash', None)
        print(user)

if __name__ == "__main__":
    get_all_users()
