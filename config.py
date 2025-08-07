import os
from dotenv import load_dotenv

load_dotenv()

BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

RSS_FEEDS = os.getenv('RSS_FEEDS', 
    'https://www.bbc.com/arabic/index.xml,'
    'https://arabic.sputniknews.com/export/rss2/archive/index.xml,'
    'https://m.youm7.com/rss/SectionRss?SectionID=88,'
    'https://www.al-mala3b.net/rss.php?type=news&id=37,'
    'https://www.al-mala3b.net/rss.php?type=news&id=38,'
    'https://www.al-mala3b.net/rss.php?type=news&id=1,'
    'https://arabic.rt.com/rss,'
    'https://www.alarabiya.net/feed/rss2/ar.xml,'
    'https://www.alarabiya.net/feed/rss2/ar/technology.xml'
).split(',')

MIN_ARTICLE_LENGTH = int(os.getenv('MIN_ARTICLE_LENGTH', '500'))
MAX_ARTICLE_LENGTH = int(os.getenv('MAX_ARTICLE_LENGTH', '2000'))
CATEGORIES_LIMIT = 5
DESCRIPTION_LENGTH = 160

DAILY_RUN_TIME = os.getenv('SCHEDULE_TIME', "18:00")
TIMEZONE = os.getenv('TIMEZONE', 'UTC')
