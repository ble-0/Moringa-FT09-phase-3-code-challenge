

import sqlite3

class Article:
    def __init__(self, author, magazine, title, content, id=None):
        # Title validation
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        # Content validation
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string.")
        
        self._author = author
        self._magazine = magazine
        self._title = title
        self._content = content
        self._id = id
        
        if id is None:  # Only insert into DB if not loading from DB
            # Use context manager for better handling of DB connection
            with sqlite3.connect('./database/magazine.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO articles (author_id, magazine_id, title, content)
                    VALUES (?, ?, ?, ?)
                """, (author.id, magazine.id, title, content))
                self._id = cursor.lastrowid
                connection.commit()

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return f'<Article {self.title} by {self.author.name}>'

    def magazines(self):
        # This method fetches all distinct magazines associated with this article's author
        connection = sqlite3.connect('./database/magazine.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self._author.id,))
        magazines = cursor.fetchall()
        connection.close()
        return magazines
