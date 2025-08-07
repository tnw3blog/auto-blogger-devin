"""
Tests for ContentGenerator
"""

import unittest
from src.content_generator import ContentGenerator

class TestContentGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = ContentGenerator()
        self.sample_topic = {
            'title': 'Test Topic',
            'content': 'Test content for the topic',
            'source': 'test',
            'score': 100,
            'url': 'https://example.com'
        }
    
    def test_init(self):
        """Test ContentGenerator initialization"""
        self.assertIsInstance(self.generator.arabic_categories, list)
        self.assertTrue(len(self.generator.arabic_categories) > 0)
    
    def test_generate_title(self):
        """Test title generation"""
        title = self.generator._generate_title(self.sample_topic)
        
        self.assertIsInstance(title, str)
        self.assertTrue(len(title) > 0)
        self.assertIn(self.sample_topic['title'], title)
    
    def test_generate_categories(self):
        """Test category generation"""
        categories = self.generator._generate_categories(self.sample_topic)
        
        self.assertIsInstance(categories, str)
        self.assertTrue(len(categories) > 0)
        self.assertIn(',', categories)
    
    def test_generate_description(self):
        """Test meta description generation"""
        content = "<p>This is test content for description generation.</p>"
        description = self.generator._generate_description(self.sample_topic, content)
        
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) <= 160)  # Meta description limit
    
    def test_generate_article(self):
        """Test complete article generation"""
        article = self.generator.generate_article(self.sample_topic)
        
        self.assertIsNotNone(article)
        if article:  # Type guard to ensure article is not None
            self.assertIn('title', article)
            self.assertIn('content', article)
            self.assertIn('categories', article)
            self.assertIn('description', article)
            
            self.assertIn('<p>', article['content'])
            self.assertIn('</p>', article['content'])

if __name__ == '__main__':
    unittest.main()
