
import sqlite3

class Magazine:
    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        self._name = name
        self._category = category
        self._id = id
        
        if id is None:  # Only insert into DB if not loading from DB
            with sqlite3.connect('./database/magazine.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
                self._id = cursor.lastrowid
                connection.commit()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def articles(self):
        # Fetch articles for this magazine
        with sqlite3.connect('./database/magazine.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM articles WHERE magazine_id = ?
            """, (self._id,))
            articles = cursor.fetchall()
        return articles

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def contributors(self):
        # Fetch distinct authors (contributors) for this magazine
        with sqlite3.connect('./database/magazine.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self._id,))
            authors = cursor.fetchall()
        return authors

