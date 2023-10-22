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
    genre_list = books.genres()
    
    if request.method == "GET":
        return render_template("add_book.html", genre_list=genre_list)
    
    if request.method == "POST":
        users.csrf_check()
        name = request.form["name"]
        year = request.form["year"]
        author = request.form["author"]
        synopsis = request.form["synopsis"]
        genres = request.form.getlist("genres[]")

        cover = request.files ["cover"]

        if not year.isnumeric():
            error = "Publication year must be a number."
            return render_template("add_book.html", error=error, genre_list=genre_list)

        if cover.filename != "":
            upload_folder = "static"
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(cover.filename)
            cover.save(os.path.join(upload_folder, filename))

            cover_path = os.path.join(upload_folder, filename)
        else:
            cover_path = None

        books.add_book(name, year, author, synopsis, cover_path)
        book = books.book(name)
        genre_list = books.genres()

        for selected_genre in genres:
            for genre in genre_list:
                if selected_genre == genre.name:
                    books.add_genres(book.id, genre.id)

        return redirect(f"/book/{name}")
    
@app.route("/book/<name>", methods=["POST", "GET"])       
def book(name):
    book = books.book(name)
    genres = books.get_genres(book.id)
    reviews = sorted(books.get_reviews(book.id), reverse=True)
    average_rating = 0
    if len(reviews) > 0:
        average_rating = books.average_rating(book.id)
    return render_template("book_info.html", book=book, genres=genres, reviews=reviews, average_rating=average_rating)

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
            if users.is_admin(username):
                session["admin"] = username
            session["csrf_token"] = secrets.token_hex(16)

            return redirect("/")
        else:
            error = login_check
            return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    del session["username"]
    if "admin" in session:
        print("test")
        del session["admin"]

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "GET":
        return render_template("register.html", error=error)
    
    if request.method == "POST":
        all_usernames = users.get_all_usernames()
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if username in all_usernames:
            error = "Username has already been taken"
        elif password != password2:
            error = "Passwords do not match"
        else:
            users.register(username, password)
            session["username"] = username
            return redirect("/")
    
    return render_template("register.html", error=error)


@app.route("/results", methods=["GET"])
def results():
    query = request.args["query"]
    search_option = request.args.getlist("search_option")
    search_results = books.search(query, search_option)
    return render_template("results.html", search_results=search_results, query=query)

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form["id"]
    books.delete_book(id)
    return redirect("/")

@app.route("/delete_review", methods=["POST"])
def delete_review():
    id = request.form["id"]
    books.delete_review(id)
    return redirect(request.referrer)

@app.route("/add_review/<name>", methods=["GET", "POST"])
def add_review(name):
    book_info = books.book(name)
    if request.method == "GET":
        return render_template("add_review.html", book_info=book_info)
    
    if request.method == "POST":
        users.csrf_check()
        rating = int(request.form["rating"])
        review = request.form["review"]

        username = session["username"]
        books.add_review(username, book_info.id, rating, review)
        return redirect(f"/book/{name}")