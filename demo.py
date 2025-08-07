#!/usr/bin/env python3
"""
Demo script for Auto Blogger Devin
عرض توضيحي لـ Auto Blogger Devin
"""

import json
from datetime import datetime
from src.trend_analyzer import TrendAnalyzer
from src.content_generator import ContentGenerator

def demo_trend_analysis():
    """عرض توضيحي لتحليل المواضيع المتداولة"""
    print("🔍 عرض توضيحي: تحليل المواضيع المتداولة")
    print("=" * 50)
    
    analyzer = TrendAnalyzer()
    
    sample_topics = [
        {
            'title': 'الذكاء الاصطناعي في الطب',
            'content': 'تطبيقات الذكاء الاصطناعي تحدث ثورة في مجال الطب من خلال تحسين التشخيص والعلاج.',
            'source': 'google_trends',
            'score': 95,
            'url': 'https://example.com/ai-medicine',
            'timestamp': datetime.now()
        },
        {
            'title': 'التقنيات المالية الجديدة',
            'content': 'البنوك الرقمية والعملات المشفرة تغير وجه الخدمات المالية التقليدية.',
            'source': 'rss_feed',
            'score': 88,
            'url': 'https://example.com/fintech',
            'timestamp': datetime.now()
        },
        {
            'title': 'الطاقة المتجددة في المنطقة',
            'content': 'مشاريع الطاقة الشمسية وطاقة الرياح تشهد نمواً متسارعاً في المنطقة العربية.',
            'source': 'rss_feed',
            'score': 82,
            'url': 'https://example.com/renewable-energy',
            'timestamp': datetime.now()
        }
    ]
    
    print(f"✅ تم العثور على {len(sample_topics)} موضوع متداول:")
    for i, topic in enumerate(sample_topics, 1):
        print(f"{i}. {topic['title']} (النقاط: {topic['score']})")
    
    return sample_topics

def demo_content_generation(topics):
    """عرض توضيحي لإنشاء المحتوى"""
    print("\n✍️ عرض توضيحي: إنشاء المحتوى")
    print("=" * 50)
    
    generator = ContentGenerator()
    
    selected_topic = topics[0]
    print(f"📰 الموضوع المختار: {selected_topic['title']}")
    
    article = generator.generate_article(selected_topic)
    
    if article:
        print("\n✅ تم إنشاء المقال بنجاح!")
        print(f"📝 العنوان: {article['title']}")
        print(f"🏷️ التصنيفات: {article['categories']}")
        print(f"📄 الوصف: {article['description']}")
        print(f"📊 طول المحتوى: {len(article['content'])} حرف")
        
        print("\n🔧 بنية HTML للمحتوى:")
        content_preview = article['content'][:500] + "..." if len(article['content']) > 500 else article['content']
        print(content_preview)
        
        return article
    else:
        print("❌ فشل في إنشاء المقال")
        return None

def demo_blogger_simulation(article):
    """محاكاة نشر المقال على Blogger"""
    print("\n📤 عرض توضيحي: محاكاة النشر على Blogger")
    print("=" * 50)
    
    if not article:
        print("❌ لا يوجد مقال للنشر")
        return
    
    print("🔐 محاكاة المصادقة مع Google API...")
    print("✅ تم تسجيل الدخول بنجاح")
    
    print("📝 تحضير المنشور...")
    post_data = {
        'title': article['title'],
        'content': article['content'],
        'labels': article['categories'].split(', '),
        'status': 'PUBLISHED'
    }
    
    print("📤 محاكاة النشر...")
    print("✅ تم نشر المقال بنجاح!")
    print(f"🔗 رابط المقال: https://your-blog.blogspot.com/2024/01/sample-post")
    
    print("\n📋 ملخص المنشور:")
    print(f"العنوان: {post_data['title']}")
    print(f"التصنيفات: {', '.join(post_data['labels'])}")
    print(f"الحالة: {post_data['status']}")

def demo_scheduling():
    """عرض توضيحي للجدولة"""
    print("\n⏰ عرض توضيحي: الجدولة التلقائية")
    print("=" * 50)
    
    print("📅 إعداد الجدولة اليومية:")
    print("- التوقيت: 9:00 صباحاً يومياً")
    print("- المهام: البحث → إنشاء المحتوى → النشر")
    print("- السجلات: حفظ في ملف auto_blogger.log")
    
    print("\n🔄 خيارات التشغيل:")
    print("1. تشغيل يدوي: python main.py")
    print("2. تشغيل مجدول: python cli.py schedule")
    print("3. اختبار المكونات: python test_components.py")
    print("4. عرض الحالة: python cli.py status")

def main():
    """تشغيل العرض التوضيحي الكامل"""
    print("🚀 مرحباً بك في Auto Blogger Devin")
    print("مولد المحتوى التلقائي للمدونات العربية")
    print("=" * 60)
    
    try:
        topics = demo_trend_analysis()
        
        article = demo_content_generation(topics)
        
        demo_blogger_simulation(article)
        
        demo_scheduling()
        
        print("\n🎉 انتهى العرض التوضيحي!")
        print("\nللبدء الفعلي:")
        print("1. قم بإعداد ملف .env بمعلومات API")
        print("2. شغل: python setup.py")
        print("3. اختبر: python test_components.py")
        print("4. شغل: python main.py")
        
    except Exception as e:
        print(f"\n❌ خطأ في العرض التوضيحي: {str(e)}")

if __name__ == "__main__":
    main()
