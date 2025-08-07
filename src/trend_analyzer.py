"""
Trend Analyzer - يحلل المواضيع الأكثر تداولاً من Google Trends و RSS feeds
"""

import logging
import requests
import feedparser
from pytrends.request import TrendReq
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import random

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    def __init__(self):
        self.pytrends = TrendReq(hl='ar', tz=360)
        self.rss_feeds = [
            'https://feeds.bbci.co.uk/arabic/rss.xml',
            'https://www.aljazeera.net/xml/rss/all.xml',
            'https://arabic.rt.com/rss',
            'https://www.alarabiya.net/ar/rss.xml'
        ]
        
    def get_trending_topics(self) -> List[Dict]:
        """الحصول على المواضيع الأكثر تداولاً"""
        trending_topics = []
        
        google_trends = self._get_google_trends()
        trending_topics.extend(google_trends)
        
        rss_topics = self._get_rss_trending()
        trending_topics.extend(rss_topics)
        
        trending_topics = self._rank_topics(trending_topics)
        
        return trending_topics[:10]  # Return top 10
    
    def _get_google_trends(self) -> List[Dict]:
        """الحصول على المواضيع المتداولة من Google Trends"""
        try:
            trending_searches = self.pytrends.trending_searches(pn='saudi_arabia')
            
            topics = []
            for search_term in trending_searches.head(20)[0]:  # Top 20 trends
                topics.append({
                    'title': search_term,
                    'source': 'google_trends',
                    'score': 100,  # High score for trending
                    'content': f"موضوع متداول: {search_term}",
                    'url': f"https://www.google.com/search?q={search_term}",
                    'timestamp': datetime.now()
                })
                
            logger.info(f"✅ تم الحصول على {len(topics)} موضوع من Google Trends")
            return topics
            
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على Google Trends: {str(e)}")
            return []
    
    def _get_rss_trending(self) -> List[Dict]:
        """الحصول على المواضيع من RSS feeds"""
        topics = []
        
        for feed_url in self.rss_feeds:
            try:
                logger.info(f"📡 جاري تحليل RSS: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Top 5 from each feed
                    pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') and entry.published_parsed else datetime.now()
                    hours_old = (datetime.now() - pub_date).total_seconds() / 3600
                    recency_score = max(0, 100 - hours_old)  # Newer = higher score
                    
                    topics.append({
                        'title': entry.title,
                        'source': feed_url.split('//')[1].split('/')[0],
                        'score': recency_score,
                        'content': getattr(entry, 'summary', entry.title),
                        'url': entry.link,
                        'timestamp': pub_date
                    })
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ خطأ في تحليل RSS {feed_url}: {str(e)}")
                continue
        
        logger.info(f"✅ تم الحصول على {len(topics)} موضوع من RSS feeds")
        return topics
    
    def _rank_topics(self, topics: List[Dict]) -> List[Dict]:
        """ترتيب المواضيع حسب الأهمية والحداثة"""
        ranked_topics = sorted(topics, key=lambda x: x['score'], reverse=True)
        
        unique_topics = []
        seen_titles = set()
        
        for topic in ranked_topics:
            title_words = set(topic['title'].lower().split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.lower().split())
                if len(title_words & seen_words) / len(title_words | seen_words) > 0.6:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_topics.append(topic)
                seen_titles.add(topic['title'])
        
        return unique_topics
    
    def get_topic_details(self, topic: Dict) -> Dict:
        """الحصول على تفاصيل إضافية للموضوع"""
        try:
            if topic['source'] != 'google_trends':
                return topic
            
            search_query = topic['title']
            
            topic['content'] = f"موضوع متداول حول {search_query}. يتطلب بحث إضافي للحصول على المحتوى الكامل."
            
            return topic
            
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على تفاصيل الموضوع: {str(e)}")
            return topic
