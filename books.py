from sqlalchemy import text
from app import db

def all_books():
    sql = "SELECT name FROM books"
    result = db.session.execute(text(sql))
    return result.fetchall()

def book(name):
    sql = "SELECT id, name, year, author, synopsis, cover FROM books WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    return result.fetchone()

def add_book(name:str, year:int, author:str, synopsis:str, cover_path):
    sql = "INSERT INTO books (name, year, author, synopsis, cover) VALUES (:name, :year, :author, :synopsis, :cover)"
    db.session.execute(text(sql), {"name":name, "year":year, "author":author, "synopsis":synopsis, "cover":cover_path})
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
    book_genres = [row[0] for row in result.fetchall()]
    return book_genres

def search(query, search_option):
    if len(search_option)==1:
        if search_option[0] == "name":
            sql = "SELECT name FROM books WHERE LOWER(name) LIKE LOWER(:query)"
        elif search_option[0] == "synopsis":
            sql = "SELECT name FROM books WHERE LOWER(synopsis) LIKE LOWER(:query)"
    else:
        sql = "SELECT name FROM books WHERE LOWER(name) LIKE LOWER(:query) OR LOWER(synopsis) LIKE LOWER(:query)"


    result = db.session.execute(text(sql), {"query":"%"+query+"%"})        
    search_results = [row[0] for row in result.fetchall()]
    return search_results

def delete_book(id):
    sql = "DELETE FROM book_genres WHERE book_id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    sql = "DELETE FROM books WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def add_review(username, book_id, rating, review):
    sql = "INSERT INTO reviews (username, book_id, rating, review) VALUES (:username, :book_id, :rating, :review)"
    db.session.execute(text(sql), {"username":username, "book_id":book_id, "rating":rating, "review":review})
    db.session.commit()

def get_reviews(book_id):
    sql = "SELECT R.id, R.username, R.book_id, R.rating, R.review FROM reviews R, books B WHERE R.book_id = B.id AND B.id=:book_id"
    result = db.session.execute(text(sql), {"book_id":book_id})
    reviews = result.fetchall()
    return reviews

def delete_review(id):
    sql = "DELETE FROM reviews WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def average_rating(book_id):
    sql = "SELECT ROUND(AVG(rating), 2) FROM reviews WHERE book_id=:book_id"
    result = db.session.execute(text(sql), {"book_id":book_id})
    avg = result.scalar()
    return str(avg)
    