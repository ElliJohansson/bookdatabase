from app import db
from flask import request, session
from sqlalchemy import text

def all_books():
    sql = "SELECT name FROM books"
    result = db.session.execute(text(sql))
    return result.fetchall()

def book(name):
    sql = "SELECT name, year, author, synopsis FROM books WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    return result.fetchone()

def add_book(name:str, year:int, author:str, synopsis:str):
    sql = "INSERT INTO books (name, year, author, synopsis) VALUES (:name, :year, :author, :synopsis)"
    db.session.execute(text(sql), {"name":name, "year":year, "author":author, "synopsis":synopsis})
    db.session.commit()