from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config 
from datetime import datetime

client = MongoClient(Config.MONGO_URI)
db = client["users"]
users_collection = db["users_collection"] 
portfolio_collection = db["portfolios"]

def get_user(username):
    return users_collection.find_one({"username": username})

def username_exists(username):
    return bool(get_user(username))

def create_user(username, password):
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password}) 
def pcreate_user(username, firstname, lastname, email, phone, school, college, skills, about, instagram, github, profile_pic, template,projects,achievements):
    return {
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phone": phone,
        "school": school,
        "college": college,
        "skills": skills or [],
        "about": about,
        "instagram": instagram,
        "github": github,
        "profile_pic": profile_pic,
        "template": template,
        "achievements":achievements,
        "projects":projects or [],
        "created_at": datetime.utcnow()
    }

def pinsert_user(db, user_data):
    db.update_one({"username": user_data["username"]}, {"$set": user_data}, upsert=True)

def pget_user(db, username):
    return db.find_one({"username": username})

