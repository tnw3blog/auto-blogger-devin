#!/usr/bin/env python3
"""
Test script for Auto Blogger Devin components
"""

import logging
import sys
from src.trend_analyzer import TrendAnalyzer
from src.content_generator import ContentGenerator
from src.blogger_publisher import BloggerPublisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_trend_analyzer():
    """اختبار محلل المواضيع المتداولة"""
    print("\n🧪 اختبار محلل المواضيع المتداولة...")
    
    try:
        analyzer = TrendAnalyzer()
        topics = analyzer.get_trending_topics()
        
        if topics:
            print(f"✅ تم العثور على {len(topics)} موضوع متداول")
            print(f"أول موضوع: {topics[0]['title']}")
            return topics[0]
        else:
            print("⚠️ لم يتم العثور على مواضيع متداولة")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في اختبار محلل المواضيع: {str(e)}")
        return None

def test_content_generator(sample_topic=None):
    """اختبار مولد المحتوى"""
    print("\n🧪 اختبار مولد المحتوى...")
    
    if not sample_topic:
        sample_topic = {
            'title': 'التقنيات الحديثة في التعليم',
            'content': 'موضوع تجريبي حول استخدام التقنيات الحديثة في التعليم',
            'source': 'test',
            'score': 100,
            'url': 'https://example.com'
        }
    
    try:
        generator = ContentGenerator()
        article = generator.generate_article(sample_topic)
        
        if article:
            print("✅ تم إنشاء المقال بنجاح")
            print(f"العنوان: {article['title']}")
            print(f"التصنيفات: {article['categories']}")
            print(f"الوصف: {article['description']}")
            return article
        else:
            print("❌ فشل في إنشاء المقال")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في اختبار مولد المحتوى: {str(e)}")
        return None

def test_blogger_publisher():
    """اختبار ناشر Blogger"""
    print("\n🧪 اختبار ناشر Blogger...")
    
    try:
        publisher = BloggerPublisher()
        
        if publisher.test_connection():
            print("✅ تم الاتصال بـ Blogger API بنجاح")
            return True
        else:
            print("❌ فشل الاتصال بـ Blogger API")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار ناشر Blogger: {str(e)}")
        print("💡 تأكد من إعداد متغيرات البيئة والمصادقة")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار مكونات Auto Blogger Devin")
    
    sample_topic = test_trend_analyzer()
    
    article = test_content_generator(sample_topic)
    
    blogger_ready = test_blogger_publisher()
    
    print("\n📊 ملخص الاختبارات:")
    print(f"محلل المواضيع: {'✅' if sample_topic else '❌'}")
    print(f"مولد المحتوى: {'✅' if article else '❌'}")
    print(f"ناشر Blogger: {'✅' if blogger_ready else '❌'}")
    
    if sample_topic and article:
        print("\n✅ جميع المكونات الأساسية تعمل بشكل صحيح")
        if not blogger_ready:
            print("⚠️ يتطلب إعداد Blogger API للنشر الفعلي")
    else:
        print("\n❌ بعض المكونات تحتاج إلى إصلاح")

if __name__ == "__main__":
    main()
