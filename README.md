# Book Database

The site is used to store and sort through information about books.

### Features at the moment

- Users can create new accounts and log in
- Logged in users can add books to the site (title, publication year, author, synopsis, genre(s), cover art)
- Users can view books on the site
- Users can search a book by a word in the name, synopsis, or both
- Admins can remove books from the site
- Logged in users can review books on the site (rating & written review)
- Users can view individual ratings and reviews, as well as the average rating, on the book's site
  
### Features

- Admins can remove reviews from the site
- Users can sort the books by rating
- Users can filter the books by genre or author

### Test in production

Requires psql.

1. ```git clone git@github.com:ElliJohansson/bookdatabase.git```
 
2. ```cd bookdatabase```

3. Create .env file (```touch .env```), and add the following in it:

   ```
   DATABASE_URL=<database-url>
   SECRET_KEY=<secret-key>
   ```

4. ```python3 -m venv venv```

5. ```source venv/bin/activate```
 
6.  ```pip install -r requirements.txt```

7. ```psql < schema.sql```

8.  ```flask run```

***

To make an admin account, first create an account. Then edit the *users* SQL table in ```psql``` as follows:
 
 ```
   UPDATE users
   SET is_admin = True
   WHERE username = '<username>';
   ```
  Then log out and back in.
