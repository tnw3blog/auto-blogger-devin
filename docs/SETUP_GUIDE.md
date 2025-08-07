# دليل الإعداد - Auto Blogger Devin

## المتطلبات الأساسية

### 1. Python و المكتبات
```bash
# تأكد من وجود Python 3.8+
python3 --version

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 2. إعداد Google API

#### أ. إنشاء مشروع في Google Cloud Console
1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. أنشئ مشروع جديد أو اختر مشروع موجود
3. فعل Blogger API v3

#### ب. إنشاء OAuth 2.0 Credentials
1. اذهب إلى "APIs & Services" > "Credentials"
2. انقر "Create Credentials" > "OAuth client ID"
3. اختر "Desktop application"
4. احفظ Client ID و Client Secret

#### ج. الحصول على Blog ID
1. اذهب إلى مدونتك على Blogger
2. من الإعدادات، انسخ Blog ID من الرابط

### 3. إعداد ملف البيئة

```bash
# انسخ ملف المثال
cp .env.example .env

# حرر الملف وأضف معلوماتك
nano .env
```

املأ المتغيرات التالية:
```
BLOGGER_BLOG_ID=your_blog_id_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## التشغيل

### 1. الإعداد الأولي
```bash
python setup.py
```

### 2. اختبار المكونات
```bash
python test_components.py
```

### 3. التشغيل اليدوي
```bash
python main.py
```

### 4. الجدولة التلقائية

#### استخدام crontab (Linux/Mac)
```bash
# فتح crontab
crontab -e

# إضافة السطر التالي للتشغيل يومياً في 9 صباحاً
0 9 * * * cd /path/to/auto-blogger-devin && python3 main.py
```

#### استخدام Task Scheduler (Windows)
1. افتح Task Scheduler
2. أنشئ مهمة جديدة
3. اضبط التوقيت على يومي
4. اضبط الإجراء على تشغيل Python script

## استكشاف الأخطاء

### خطأ في المصادقة
- تأكد من صحة Client ID و Client Secret
- تأكد من تفعيل Blogger API
- احذف token.json وأعد المصادقة

### خطأ في Blog ID
- تأكد من صحة Blog ID
- تأكد من أن الحساب له صلاحية الكتابة في المدونة

### خطأ في الشبكة
- تحقق من الاتصال بالإنترنت
- تحقق من عدم حجب APIs

## الميزات المتقدمة

### إضافة مصادر RSS جديدة
حرر `config.py` وأضف روابط RSS:
```python
RSS_FEEDS = [
    'https://feeds.bbci.co.uk/arabic/rss.xml',
    'https://your-new-feed.com/rss.xml'
]
```

### تخصيص القوالب
حرر `src/content_generator.py` لتخصيص:
- قوالب العناوين
- تنسيق المحتوى
- التصنيفات

### إضافة مصادر صور
يمكن ربط APIs مجانية للصور مثل:
- Unsplash API
- Pixabay API
- Pexels API
