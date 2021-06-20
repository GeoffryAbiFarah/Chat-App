from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config["DB_URL"])

chat_db = client.get_database("ChatAppDB")
users_collection = chat_db.get_collection("users")

def save_user(username, email, password):
    users_collection.insert_one({
        "_id": username,
        "email": email,
        "password": generate_password_hash(password)
    })

save_user("steph", "geoffry_abifarah@hotmail.com","test")