from app import db
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    
    if not user:
        return "Invalid username"
    
    hash_value = user.password

    if not check_password_hash(hash_value, password):
        return "Invalid password"
    else:
        return True
        

def register(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
