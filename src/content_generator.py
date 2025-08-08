import logging
import requests
import os
from typing import Dict, Optional
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
        try:
            logger.info(f"✍️ إنشاء مقال للموضوع: {topic['title']}")

            title = self._generate_title(topic)

            intro = self._generate_introduction(topic)
            main_content = self._generate_content(topic)
            conclusion = self._generate_conclusion(topic)

            # الصورة تأتي من المصدر الأصلي فقط، توضع في نهاية المقال مع حقوق المصدر
            image_html = self._get_article_image(topic)

            # دمج المحتوى مع المقدمة والخاتمة والصورة في النهاية
            full_content = f"{intro}\n{main_content}\n{conclusion}\n{image_html}"

            categories = self._generate_categories(topic)
            description = self._generate_description(topic, main_content)

            article = {
                'title': title,
                'content': full_content.strip(),
                'image_html': image_html,  # ممكن حذف هذا المفتاح إذا غير ضروري
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
        return topic['title']

    def _generate_content(self, topic: Dict) -> str:
        full_content = self._extract_full_article_content(topic.get('url', ''))

        if not full_content:
            full_content = topic.get('content', topic['title'])

        # تنظيف وتنسيق المحتوى الأصلي بالكامل (بدون اقتصاص 50%)
        formatted_content = self._format_main_content(full_content)

        # إضافة رابط المصدر في نهاية المحتوى
        if topic.get('url'):
            formatted_content += f'\n<p><a href="{topic["url"]}" target="_blank" rel="noopener">اقرأ المزيد من المصدر الأصلي</a></p>'

        return formatted_content.strip()

    def _format_main_content(self, content: str) -> str:
        # تقسيم المحتوى إلى فقرات ثم تنسيق كل فقرة داخل <p>
        soup = BeautifulSoup(content, 'html.parser')
        clean_text = soup.get_text(separator='\n').strip()
        paragraphs = [p.strip() for p in clean_text.split('\n') if p.strip()]

        formatted_paragraphs = [f"<p>{p}</p>" for p in paragraphs]

        return '\n'.join(formatted_paragraphs)

    def _generate_introduction(self, topic: Dict) -> str:
        intros = [
            f"<p><i>يشهد موضوع <b>{topic['title']}</b> اهتماماً متزايداً في الآونة الأخيرة، حيث تتابع وسائل الإعلام والجمهور التطورات بشكل مستمر.</i></p>",
            f"<p><i>في ظل الأحداث الجارية، يبرز موضوع <b>{topic['title']}</b> كأحد أهم القضايا التي تستحق المتابعة والتحليل.</i></p>",
            f"<p><i>تتزايد أهمية فهم <b>{topic['title']}</b> في السياق الحالي، خاصة مع التطورات السريعة التي نشهدها.</i></p>",
        ]
        return random.choice(intros)

    def _generate_conclusion(self, topic: Dict) -> str:
        conclusions = [
            f"<p>يبقى موضوع <b>{topic['title']}</b> محل اهتمام ومتابعة، ومن المهم البقاء على اطلاع بآخر التطورات.</p>",
            f"<p>نستمر في متابعة <b>{topic['title']}</b> ونقدم لكم آخر المستجدات والتحليلات المتعمقة.</p>",
            f"<p>موضوع <b>{topic['title']}</b> يتطلب مزيداً من البحث والتحليل، وسنواصل تغطيته في المقالات القادمة.</p>",
        ]
        return random.choice(conclusions)

    def _get_article_image(self, topic: Dict) -> str:
        try:
            original_image = self._extract_image_from_article(topic.get('url', ''))
            if original_image:
                # صورة من المصدر الأصلي مع ذكر حقوق المصدر
                return f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{original_image}" alt="صورة تعبر عن {topic['title']}" style="max-width: 100%; height: auto; border-radius: 8px;" />
                    <p style="font-size: 12px; color: #666; margin-top: 5px;">
                        <i>حقوق الصورة محفوظة للمصدر الأصلي</i>
                    </p>
                </div>
                """
            # إذا لم توجد صورة، لا تُدرج أي صورة
            return ""
        except Exception as e:
            logger.warning(f"⚠️ لم يتم العثور على صورة مناسبة: {str(e)}")
            return ""

    def _extract_image_from_article(self, article_url: str) -> Optional[str]:
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

    def _generate_categories(self, topic: Dict) -> str:
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
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text().strip()

        first_sentence = text_content.split('.')[0].strip()
        if len(first_sentence) > 180:
            description = first_sentence[:177] + "..."
        else:
            description = first_sentence + "."

        return description.strip()

    def _extract_full_article_content(self, article_url: str) -> str:
        try:
            if not article_url:
                return ""

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(article_url, headers=headers, timeout=15)
            if response.status_code != 200:
                return ""

            soup = BeautifulSoup(response.content, 'html.parser')

            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                element.decompose()

            content_selectors = [
                'article .content',
                'article .article-content',
                '.post-content',
                '.entry-content',
                'article p',
                '.content p',
                'main p'
            ]

            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content_text = ' '.join([elem.get_text().strip() for elem in elements])
                    break

            if not content_text:
                paragraphs = soup.find_all('p')
                content_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])

            return content_text.strip()

        except Exception as e:
            logger.warning(f"⚠️ خطأ في استخراج المحتوى من {article_url}: {str(e)}")
            return ""
