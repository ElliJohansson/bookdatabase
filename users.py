from app import db
from sqlalchemy import text
from flask import session, request, abort
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
    is_admin = False
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
    db.session.execute(text(sql), {"username":username, "password":hash_value, "is_admin":is_admin})
    db.session.commit()


def csrf_check():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def is_admin(username):
    sql = "SELECT * FROM users WHERE username =:username AND is_admin = True"
    result = db.session.execute(text(sql), {"username":username})
    if result:        
        return True
    else:
        return False