# Book Database

The site is used to store and sort through information about books.

### Features at the moment

- Users can create new accounts
- Users can add books to the site (title, publication year, author, synopsis)
- Users can view books on the site

### Features

- Users can log in
- Admins can remove books and reviews from the site
- Users can review books on the site and view the average rating
- Users can sort the books by rating
- Users can filter the books by genre or author

### Test in production

Requires psql.

 ```git clone git@github.com:ElliJohansson/bookdatabase.git```
 
 ```cd bookdatabase```

 ```python3 -m venv venv```

 ```source venv/bin/activate```
 
 ```pip install -r requirements.txt```

```psql < schema.sql```

 ```flask run```
