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
from urllib.parse import urljoin, urlparse

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
        """تنظيف المحتوى الأصلي واستخدام نصف المحتوى فقط"""
        soup = BeautifulSoup(content, 'html.parser')
        clean_text = soup.get_text()
        
        sentences = clean_text.split('.')
        
        half_content_sentences = sentences[:max(3, len(sentences)//2)]
        half_content = '. '.join(half_content_sentences).strip()
        
        if half_content and not half_content.endswith('.'):
            half_content += '.'
        
        return half_content
    
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
        """الحصول على صورة من المقال الأصلي أو مصدر بديل"""
        try:
            original_image = self._extract_image_from_article(topic.get('url', ''))
            if original_image:
                return f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{original_image}" 
                         alt="{topic['title']}" 
                         style="max-width: 100%; height: auto; border-radius: 8px;" />
                    <p style="font-size: 12px; color: #666; margin-top: 5px;">
                        <i>حقوق الصورة محفوظة للمصدر الأصلي</i>
                    </p>
                </div>
                """
            
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
                            <i>حقوق الصورة محفوظة للمصدر الأصلي</i>
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
                    <i>حقوق الصورة محفوظة للمصدر الأصلي</i>
                </p>
            </div>
            """
            
        except Exception as e:
            logger.warning(f"⚠️ لم يتم العثور على صورة مناسبة: {str(e)}")
            return ""
    
    def _extract_image_from_article(self, article_url: str) -> Optional[str]:
        """استخراج الصورة من المقال الأصلي"""
        try:
            if not article_url:
                return None
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(article_url, headers=headers, timeout=10)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            image_selectors = [
                'article img',
                '.article-content img',
                '.content img',
                '.post-content img',
                'img[src*="jpg"]',
                'img[src*="jpeg"]',
                'img[src*="png"]',
                'img[src*="webp"]'
            ]
            
            for selector in image_selectors:
                images = soup.select(selector)
                for img in images:
                    src = img.get('src') or img.get('data-src')
                    if src and self._is_valid_image_url(src):
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            parsed_url = urlparse(article_url)
                            src = f"{parsed_url.scheme}://{parsed_url.netloc}{src}"
                        elif not src.startswith('http'):
                            src = urljoin(article_url, src)
                        
                        return src
            
        except Exception as e:
            logger.warning(f"⚠️ خطأ في استخراج الصورة من {article_url}: {str(e)}")
        
        return None
    
    def _is_valid_image_url(self, url: str) -> bool:
        """التحقق من صحة رابط الصورة"""
        if not url:
            return False
        
        invalid_patterns = [
            'logo', 'icon', 'avatar', 'profile', 'thumbnail',
            'banner', 'header', 'footer', 'sidebar', 'widget'
        ]
        
        url_lower = url.lower()
        for pattern in invalid_patterns:
            if pattern in url_lower:
                return False
        
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        return any(ext in url_lower for ext in valid_extensions)

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
