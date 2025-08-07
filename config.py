import os
from dotenv import load_dotenv

load_dotenv()

BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

RSS_FEEDS = [
    'https://feeds.bbci.co.uk/arabic/rss.xml',
    'https://www.aljazeera.net/xml/rss/all.xml',
    'https://arabic.rt.com/rss',
    'https://www.alarabiya.net/ar/rss.xml'
]

MIN_ARTICLE_LENGTH = 500
MAX_ARTICLE_LENGTH = 2000
CATEGORIES_LIMIT = 5
DESCRIPTION_LENGTH = 160

DAILY_RUN_TIME = "09:00"
