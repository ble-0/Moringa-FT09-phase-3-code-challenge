import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe", 1)
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        # Ensure content is a valid string and passed in the correct position
        article = Article(1, "Tech Weekly", "Test Title", "Some content here", 1)
    
         # Add assertions to check if the object is created as expected
        assert article.title == "Test Title"
        assert article.content == "Some content here"



    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Category")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()

