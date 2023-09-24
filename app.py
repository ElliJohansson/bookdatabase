from os import getenv
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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