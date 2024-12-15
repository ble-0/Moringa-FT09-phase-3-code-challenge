import sqlite3

class Author:
    def __init__(self, name, id=None):
        # Validate name
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        
        self._name = name
        self._id = id
        
        # Insert into the DB if the author doesn't already have an ID
        if id is None:
            with sqlite3.connect('./database/magazine.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
                self._id = cursor.lastrowid
                connection.commit()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        # Fetch all articles written by this author
        with sqlite3.connect('./database/magazine.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
            articles = cursor.fetchall()
        return articles

    def __repr__(self):
        return f'<Author {self.name}>'

    def magazines(self):
        # Fetch all distinct magazines associated with this author
        with sqlite3.connect('./database/magazine.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self._id,))
            magazines = cursor.fetchall()
        return magazines
