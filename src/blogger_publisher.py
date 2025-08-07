"""
Blogger Publisher - ينشر المقالات على منصة Blogger
"""

import logging
import json
import os
from typing import Dict, Optional
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config

logger = logging.getLogger(__name__)

class BloggerPublisher:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/blogger']
        self.blog_id = config.BLOGGER_BLOG_ID
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """المصادقة مع Google API"""
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                self._create_credentials_file()
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('blogger', 'v3', credentials=creds)
        logger.info("✅ تم تسجيل الدخول إلى Blogger API بنجاح")
    
    def _create_credentials_file(self):
        """إنشاء ملف credentials.json من متغيرات البيئة"""
        credentials_data = {
            "installed": {
                "client_id": config.GOOGLE_CLIENT_ID,
                "client_secret": config.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open('credentials.json', 'w') as f:
            json.dump(credentials_data, f)
    
    def publish_article(self, article: Dict) -> bool:
        """نشر المقال على Blogger"""
        try:
            if not self.service:
                logger.error("❌ لم يتم تسجيل الدخول إلى Blogger API")
                return False
            
            full_content = self._prepare_post_content(article)
            
            post_body = {
                'title': article['title'],
                'content': full_content,
                'labels': article['categories'].split(', '),
            }
            
            if article.get('description'):
                post_body['customMetaData'] = article['description']
                
                meta_tags = f"""<!--more-->
                <meta name="description" content="{article['description']}" />
                <meta property="og:description" content="{article['description']}" />
                <meta name="twitter:description" content="{article['description']}" />
                """
                post_body['content'] = meta_tags + post_body['content']
            
            posts = self.service.posts()
            request = posts.insert(blogId=self.blog_id, body=post_body)
            response = request.execute()
            
            post_url = response.get('url', '')
            logger.info(f"✅ تم نشر المقال بنجاح: {post_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ في نشر المقال: {str(e)}")
            return False
    
    def _prepare_post_content(self, article: Dict) -> str:
        """تحضير محتوى المنشور مع الصورة ورابط إكمال القراءة"""
        content_parts = []
        
        if article.get('image_html'):
            content_parts.append(article['image_html'])
        
        content_parts.append(article['content'])
        
        if article.get('source_url'):
            content_parts.append(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                <p style="margin: 0; font-size: 14px;">
                    <strong>📖 لإكمال قراءة المقال كاملاً:</strong><br>
                    <a href="{article['source_url']}" target="_blank" style="color: #007bff; text-decoration: none;">
                        👈 اضغط هنا للانتقال إلى المصدر الأصلي
                    </a>
                </p>
            </div>
            """)
            
            content_parts.append(f"""
            <hr>
            <p style="font-size: 12px; color: #666;">
                <i>المصدر الأصلي: <a href="{article['source_url']}" target="_blank">رابط المصدر</a></i><br>
                <i>حقوق المحتوى محفوظة للمصدر الأصلي</i>
            </p>
            """)
        
        content_parts.append("""
        <hr>
        <p style="text-align: center; font-size: 12px; color: #666;">
            <i>تم إنشاء هذا المحتوى تلقائياً بواسطة Auto Blogger Devin</i>
        </p>
        """)
        
        return '\n'.join(content_parts)
    
    def get_blog_info(self) -> Optional[Dict]:
        """الحصول على معلومات المدونة"""
        try:
            if not self.service:
                return None
            
            blogs = self.service.blogs()
            request = blogs.get(blogId=self.blog_id)
            response = request.execute()
            
            return {
                'name': response.get('name'),
                'description': response.get('description'),
                'url': response.get('url'),
                'posts_count': response.get('posts', {}).get('totalItems', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على معلومات المدونة: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """اختبار الاتصال مع Blogger API"""
        try:
            blog_info = self.get_blog_info()
            if blog_info:
                logger.info(f"✅ تم الاتصال بالمدونة: {blog_info['name']}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ فشل اختبار الاتصال: {str(e)}")
            return False
