#!/usr/bin/env python3
"""
Auto Blogger Devin - Automated Arabic Blog Content Generator
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from src.trend_analyzer import TrendAnalyzer
from src.content_generator import ContentGenerator
from src.blogger_publisher import BloggerPublisher
from src.scheduler import DailyScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_blogger.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    try:
        logger.info("🚀 بدء تشغيل Auto Blogger Devin")
        
        trend_analyzer = TrendAnalyzer()
        content_generator = ContentGenerator()
        blogger_publisher = BloggerPublisher()
        
        logger.info("📈 البحث عن المواضيع الأكثر تداولاً...")
        trending_topics = trend_analyzer.get_trending_topics()
        
        if not trending_topics:
            logger.warning("⚠️ لم يتم العثور على مواضيع متداولة")
            return
        
        selected_topic = trending_topics[0]
        logger.info(f"📰 الموضوع المختار: {selected_topic['title']}")
        
        logger.info("✍️ إنشاء المحتوى...")
        article = content_generator.generate_article(selected_topic)
        
        if not article:
            logger.error("❌ فشل في إنشاء المحتوى")
            return
        
        logger.info("📤 نشر المقال على Blogger...")
        success = blogger_publisher.publish_article(article)
        
        if success:
            logger.info("✅ تم نشر المقال بنجاح!")
        else:
            logger.error("❌ فشل في نشر المقال")
            
    except Exception as e:
        logger.error(f"❌ خطأ في التشغيل: {str(e)}")
        raise

if __name__ == "__main__":
    main()
