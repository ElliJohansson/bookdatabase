from app import db, app
from flask import request, render_template, redirect, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

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
        synopsis = request.form["synopsis"]
        sql = "INSERT INTO books (name, year, author, synopsis) VALUES (:name, :year, :author, :synopsis)"
        db.session.execute(text(sql), {"name":name, "year":year, "author":author, "synopsis":synopsis})
        db.session.commit()
        return redirect("/")  
    
@app.route("/book/<name>", methods=["POST", "GET"])       
def book(name):
    sql = "SELECT id, name, year, author, synopsis FROM books WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    book = result.fetchone()
    return render_template("book_info.html", book=book)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password == password2:
            hash_value = generate_password_hash(password)
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/")
        else:
            return "Passwords do not match"

