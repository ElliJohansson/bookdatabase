import os
from app import app
from flask import request, render_template, redirect, session
from werkzeug.utils import secure_filename
import secrets
import books
import users

@app.route("/")
def index():
    all_books = books.all_books()
    return render_template("index.html", books=all_books)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        genre_list = books.genres()
        return render_template("add_book.html", genre_list=genre_list)
    
    if request.method == "POST":
        name = request.form["name"]
        year = request.form["year"]
        author = request.form["author"]
        synopsis = request.form["synopsis"]
        genres = request.form.getlist("genres[]")

        cover = request.files ["cover"]
        if cover != None:
            upload_folder = "static"
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(cover.filename)
            cover.save(os.path.join(upload_folder, filename))

            cover_path = os.path.join(upload_folder, filename)
        else:
            cover = None

        books.add_book(name, year, author, synopsis, cover_path)
        book = books.book(name)
        genre_list = books.genres()

        for selected_genre in genres:
            for genre in genre_list:
                if selected_genre == genre.name:
                    books.add_genres(book.id, genre.id)

        return redirect("/")
    
@app.route("/book/<name>", methods=["POST", "GET"])       
def book(name):
    book = books.book(name)
    genres = books.get_genres(book.id)
    return render_template("book_info.html", book=book, genres=genres)

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
            session["csrf_token"] = secrets.token_hex(16)

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


@app.route("/results", methods=["GET"])
def results():
    search_results = books.search()
    return render_template("results.html", search_results=search_results)
