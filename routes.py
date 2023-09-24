from app import db, app
from flask import request, render_template, redirect
from sqlalchemy import text

@app.route("/")
def index():
    result = db.session.execute(text("SELECT name, year, author FROM books"))
    books = result.fetchall()
    return render_template("index.html", count=len(books), books=books)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    
    if request.method == "POST":
        name = request.form["name"]
        year = request.form["year"]
        author = request.form["author"]
        sql = "INSERT INTO books (name, year, author) VALUES (:name, :year, :author)"
        db.session.execute(text(sql), {"name":name, "year":year, "author":author})
        db.session.commit()
        return redirect("/")  
    
@app.route("/book/<name>", methods=["POST", "GET"])       
def book(name):
    sql = "SELECT id, name, year, author FROM books WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    book = result.fetchone()
    return f"{book}"