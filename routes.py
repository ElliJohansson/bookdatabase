from app import app
from flask import request, render_template, redirect, session
import books
import users

@app.route("/")
def index():
    all_books = books.all_books()
    return render_template("index.html", books=all_books)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    
    if request.method == "POST":
        name = request.form["name"]
        year = request.form["year"]
        author = request.form["author"]
        synopsis = request.form["synopsis"]
        books.add_book(name, year, author, synopsis)
        return redirect("/")
    
@app.route("/book/<name>", methods=["POST", "GET"])       
def book(name):
    book = books.book(name)
    return render_template("book_info.html", book=book)

@app.route("/login",methods=["GET", "POST"])
def login():
    error = None
    if request.method == "GET":
        return render_template("login.html", error=error)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        login_check = users.login(username, password)

        if login_check is True:
            session["username"] = username
            return redirect("/")
        else:
            error = login_check
            return render_template("login.html", error=error)

        



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "GET":
        return render_template("register.html", error=error)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password == password2:
            users.register(username, password)
            session["username"] = username
            return redirect("/")
        else:
            error = "Passwords do not match"
    
    return render_template("register.html", error=error)

