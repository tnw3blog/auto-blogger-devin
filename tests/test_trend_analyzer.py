"""
Tests for TrendAnalyzer
"""

import unittest
from unittest.mock import patch, MagicMock
from src.trend_analyzer import TrendAnalyzer

class TestTrendAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = TrendAnalyzer()
    
    def test_init(self):
        """Test TrendAnalyzer initialization"""
        self.assertIsNotNone(self.analyzer.pytrends)
        self.assertIsInstance(self.analyzer.rss_feeds, list)
        self.assertTrue(len(self.analyzer.rss_feeds) > 0)
    
    @patch('feedparser.parse')
    def test_get_rss_trending(self, mock_parse):
        """Test RSS trending topics extraction"""
        mock_entry = MagicMock()
        mock_entry.title = "Test News Title"
        mock_entry.summary = "Test news summary"
        mock_entry.link = "https://example.com/news"
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed = MagicMock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        topics = self.analyzer._get_rss_trending()
        
        self.assertIsInstance(topics, list)
        if topics:  # If we got results
            self.assertIn('title', topics[0])
            self.assertIn('source', topics[0])
            self.assertIn('score', topics[0])
    
    def test_rank_topics(self):
        """Test topic ranking functionality"""
        test_topics = [
            {'title': 'Topic A', 'score': 50},
            {'title': 'Topic B', 'score': 100},
            {'title': 'Topic C', 'score': 75}
        ]
        
        ranked = self.analyzer._rank_topics(test_topics)
        
        self.assertEqual(ranked[0]['score'], 100)
        self.assertEqual(ranked[1]['score'], 75)
        self.assertEqual(ranked[2]['score'], 50)

if __name__ == '__main__':
    unittest.main()
