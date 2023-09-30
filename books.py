from app import db
from flask import request, session
from sqlalchemy import text

def all_books():
    sql = "SELECT name FROM books"
    result = db.session.execute(text(sql))
    return result.fetchall()

def book(name):
    sql = "SELECT id, name, year, author, synopsis FROM books WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    return result.fetchone()

def add_book(name:str, year:int, author:str, synopsis:str):
    sql = "INSERT INTO books (name, year, author, synopsis) VALUES (:name, :year, :author, :synopsis)"
    db.session.execute(text(sql), {"name":name, "year":year, "author":author, "synopsis":synopsis})
    db.session.commit()

def genres():
    sql = "SELECT id, name FROM genres"
    result = db.session.execute(text(sql))
    return result.fetchall()

def add_genres(book_id, genre_id):
    sql = "INSERT INTO book_genres (book_id, genre_id) VALUES (:book_id, :genre_id)"
    db.session.execute(text(sql), {"book_id":book_id, "genre_id":genre_id})
    db.session.commit()

def get_genres(book_id):
    sql = "SELECT G.name FROM genres G, books B, book_genres BK WHERE G.id = BK.genre_id AND B.id = BK.book_id AND B.id=:book_id"
    result = db.session.execute(text(sql), {"book_id":book_id})
    genres = [row[0] for row in result.fetchall()]
    return genres