"""
Content Generator - ينشئ محتوى المقالات مع التنسيق المطلوب
"""

import logging
import requests
import re
import os
from typing import Dict, List, Optional
from datetime import datetime
import random
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.arabic_categories = [
            'أخبار', 'تقنية', 'رياضة', 'صحة', 'اقتصاد', 'سياسة', 
            'ثقافة', 'تعليم', 'سفر', 'طبخ', 'موضة', 'علوم'
        ]
        
    def generate_article(self, topic: Dict) -> Optional[Dict]:
        """إنشاء مقال كامل من الموضوع المحدد"""
        try:
            logger.info(f"✍️ إنشاء مقال للموضوع: {topic['title']}")
            
            title = self._generate_title(topic)
            
            content = self._generate_content(topic)
            
            image_html = self._get_article_image(topic)
            
            categories = self._generate_categories(topic)
            
            description = self._generate_description(topic, content)
            
            article = {
                'title': title,
                'content': content,
                'image_html': image_html,
                'categories': categories,
                'description': description,
                'source_url': topic.get('url', ''),
                'created_at': datetime.now()
            }
            
            logger.info("✅ تم إنشاء المقال بنجاح")
            return article
            
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء المقال: {str(e)}")
            return None
    
    def _generate_title(self, topic: Dict) -> str:
        """إنشاء عنوان مناسب للمقال"""
        original_title = topic['title']
        
        templates = [
            f"كل ما تحتاج معرفته عن {original_title}",
            f"{original_title}: التطورات الأخيرة والتحليل",
            f"تحليل شامل: {original_title}",
            f"{original_title} - الأخبار والتحديثات",
            f"آخر المستجدات حول {original_title}",
        ]
        
        return random.choice(templates)
    
    def _generate_content(self, topic: Dict) -> str:
        """إنشاء محتوى المقال مع تنسيق HTML"""
        
        original_content = topic.get('content', topic['title'])
        cleaned_content = self._clean_and_expand_content(original_content)
        
        html_content = f"""
        <p><b>مقدمة:</b></p>
        <p>{self._generate_introduction(topic)}</p>
        
        <p><b>التفاصيل الرئيسية:</b></p>
        {self._format_main_content(cleaned_content)}
        
        <p><b>النقاط المهمة:</b></p>
        {self._generate_key_points(topic)}
        
        <p><b>الخلاصة:</b></p>
        <p>{self._generate_conclusion(topic)}</p>
        """
        
        return html_content.strip()
    
    def _clean_and_expand_content(self, content: str) -> str:
        """تنظيف وتوسيع المحتوى الأصلي"""
        soup = BeautifulSoup(content, 'html.parser')
        clean_text = soup.get_text()
        
        expanded_content = f"""
        {clean_text}
        
        هذا الموضوع يحظى باهتمام واسع في الوقت الحالي، ويتطلب متابعة دقيقة للتطورات الجديدة.
        من المهم فهم السياق العام والتأثيرات المحتملة على المجتمع والاقتصاد.
        """
        
        return expanded_content
    
    def _generate_introduction(self, topic: Dict) -> str:
        """إنشاء مقدمة للمقال"""
        intros = [
            f"يشهد موضوع {topic['title']} اهتماماً متزايداً في الآونة الأخيرة، حيث تتابع وسائل الإعلام والجمهور التطورات بشكل مستمر.",
            f"في ظل الأحداث الجارية، يبرز موضوع {topic['title']} كأحد أهم القضايا التي تستحق المتابعة والتحليل.",
            f"تتزايد أهمية فهم {topic['title']} في السياق الحالي، خاصة مع التطورات السريعة التي نشهدها.",
        ]
        return random.choice(intros)
    
    def _format_main_content(self, content: str) -> str:
        """تنسيق المحتوى الرئيسي مع HTML"""
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                if i == 0:
                    formatted_paragraphs.append(f"<p><i>{paragraph.strip()}</i></p>")
                else:
                    formatted_paragraphs.append(f"<p>{paragraph.strip()}</p>")
        
        return '\n'.join(formatted_paragraphs)
    
    def _generate_key_points(self, topic: Dict) -> str:
        """إنشاء النقاط المهمة كقائمة"""
        points = [
            f"أهمية متابعة التطورات المتعلقة بـ {topic['title']}",
            "التأثير على المجتمع والاقتصاد",
            "الآراء المختلفة حول الموضوع",
            "التوقعات المستقبلية والتحليلات",
            "الدروس المستفادة والتوصيات"
        ]
        
        html_list = "<ul>\n"
        for point in points:
            html_list += f"  <li>{point}</li>\n"
        html_list += "</ul>"
        
        return html_list
    
    def _generate_conclusion(self, topic: Dict) -> str:
        """إنشاء خاتمة للمقال"""
        conclusions = [
            f"في الختام، يبقى موضوع {topic['title']} محل اهتمام ومتابعة، ومن المهم البقاء على اطلاع بآخر التطورات.",
            f"نستمر في متابعة {topic['title']} ونقدم لكم آخر المستجدات والتحليلات المتعمقة.",
            f"موضوع {topic['title']} يتطلب مزيداً من البحث والتحليل، وسنواصل تغطيته في المقالات القادمة.",
        ]
        return random.choice(conclusions)
    
    def _get_article_image(self, topic: Dict) -> str:
        """الحصول على صورة مناسبة للمقال"""
        try:
            unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY')
            if unsplash_key:
                image_url = self._get_unsplash_image(topic['title'], unsplash_key)
                if image_url:
                    return f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="{image_url}" 
                             alt="{topic['title']}" 
                             style="max-width: 100%; height: auto; border-radius: 8px;" />
                        <p style="font-size: 12px; color: #666; margin-top: 5px;">
                            <i>صورة توضيحية للموضوع</i>
                        </p>
                    </div>
                    """
            
            keywords = topic['title'].replace(' ', '+')[:50]
            image_url = f"https://source.unsplash.com/800x400/?{keywords},news,arabic"
            
            return f"""
            <div style="text-align: center; margin: 20px 0;">
                <img src="{image_url}" 
                     alt="{topic['title']}" 
                     style="max-width: 100%; height: auto; border-radius: 8px;" />
                <p style="font-size: 12px; color: #666; margin-top: 5px;">
                    <i>صورة توضيحية للموضوع</i>
                </p>
            </div>
            """
            
        except Exception as e:
            logger.warning(f"⚠️ لم يتم العثور على صورة مناسبة: {str(e)}")
            return ""
    
    def _get_unsplash_image(self, query: str, access_key: str) -> Optional[str]:
        """الحصول على صورة من Unsplash API"""
        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {access_key}"}
            params = {
                "query": query[:50],
                "per_page": 1,
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['urls']['regular']
            
        except Exception as e:
            logger.warning(f"⚠️ خطأ في Unsplash API: {str(e)}")
        
        return None
    
    def _generate_categories(self, topic: Dict) -> str:
        """إنشاء تصنيفات مناسبة للمقال"""
        content_lower = (topic['title'] + ' ' + topic.get('content', '')).lower()
        
        relevant_categories = []
        
        category_keywords = {
            'تقنية': ['تقنية', 'تكنولوجيا', 'ذكي', 'رقمي', 'إنترنت', 'تطبيق'],
            'رياضة': ['رياضة', 'كرة', 'مباراة', 'بطولة', 'لاعب'],
            'صحة': ['صحة', 'طب', 'علاج', 'مرض', 'دواء'],
            'اقتصاد': ['اقتصاد', 'مال', 'استثمار', 'بنك', 'سوق'],
            'سياسة': ['سياسة', 'حكومة', 'رئيس', 'وزير', 'انتخابات'],
            'أخبار': ['خبر', 'حدث', 'جديد', 'عاجل']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                relevant_categories.append(category)
        
        if len(relevant_categories) < 2:
            relevant_categories.extend(['أخبار', 'عام'])
        
        return ', '.join(relevant_categories[:5])
    
    def _generate_description(self, topic: Dict, content: str) -> str:
        """إنشاء وصف للبحث (meta description)"""
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text()
        
        first_sentence = text_content.split('.')[0]
        if len(first_sentence) > 160:
            description = first_sentence[:157] + "..."
        else:
            description = first_sentence + "."
        
        return description.strip()
