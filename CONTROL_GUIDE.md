# 🎛️ دليل التحكم الشامل - Auto Blogger Devin

## 📍 نقاط التحكم الرئيسية

### 1. 🔗 إدارة روابط RSS
**الموقع**: ملف `.env`
```env
RSS_FEEDS=https://feeds.bbci.co.uk/arabic/rss.xml,https://www.aljazeera.net/xml/rss/all.xml,https://arabic.rt.com/rss,https://www.alarabiya.net/ar/rss.xml
```

**كيفية الإضافة/التعديل**:
1. افتح ملف `.env`
2. أضف روابط RSS جديدة مفصولة بفواصل
3. احفظ الملف
4. أعد تشغيل النظام

**أمثلة روابط RSS عربية**:
- BBC العربية: `https://feeds.bbci.co.uk/arabic/rss.xml`
- الجزيرة: `https://www.aljazeera.net/xml/rss/all.xml`
- RT العربية: `https://arabic.rt.com/rss`
- العربية: `https://www.alarabiya.net/ar/rss.xml`
- CNN العربية: `https://arabic.cnn.com/api/v1/rss/rss.xml`

### 2. ⏰ التحكم في الجدولة
**الموقع**: ملف `.env`
```env
SCHEDULE_TIME=18:00
TIMEZONE=UTC
```

**أوقات مهمة**:
- `18:00` = 9 مساء بتوقيت السعودية
- `15:00` = 6 مساء بتوقيت السعودية  
- `12:00` = 3 عصراً بتوقيت السعودية
- `21:00` = 12 منتصف الليل بتوقيت السعودية

**تغيير التوقيت**:
1. عدّل `SCHEDULE_TIME` في ملف `.env`
2. استخدم تنسيق 24 ساعة (مثل: `20:30`)
3. احفظ وأعد تشغيل المجدول

### 3. 🖼️ التحكم في الصور
**الموقع**: ملف `.env`
```env
UNSPLASH_ACCESS_KEY=your_unsplash_key_optional
```

**خيارات الصور**:
- **بدون مفتاح**: صور تلقائية من source.unsplash.com
- **مع مفتاح Unsplash**: صور عالية الجودة من Unsplash API
- **تعطيل الصور**: اتركه فارغاً لتعطيل الصور

**الحصول على مفتاح Unsplash مجاناً**:
1. سجل في https://unsplash.com/developers
2. أنشئ تطبيق جديد
3. انسخ Access Key
4. ضعه في ملف `.env`

### 4. ✍️ التحكم في محتوى المقال
**الموقع**: `src/content_generator.py`

**تخصيص القوالب**:
```python
# تعديل قوالب العناوين (السطر 58-64)
templates = [
    f"كل ما تحتاج معرفته عن {original_title}",
    f"{original_title}: التطورات الأخيرة والتحليل",
    # أضف قوالب جديدة هنا
]

# تعديل التصنيفات (السطر 17-20)
self.arabic_categories = [
    'أخبار', 'تقنية', 'رياضة', 'صحة', 'اقتصاد', 'سياسة', 
    'ثقافة', 'تعليم', 'سفر', 'طبخ', 'موضة', 'علوم'
    # أضف تصنيفات جديدة هنا
]
```

**تخصيص طول المقال**:
```env
MIN_ARTICLE_LENGTH=500
MAX_ARTICLE_LENGTH=2000
```

### 5. 🔍 التحكم في وصف البحث (SEO)
**الموقع**: `src/content_generator.py` (السطر 193-204)

**تخصيص وصف البحث**:
- يتم إنشاؤه تلقائياً من أول جملة
- الحد الأقصى: 160 حرف
- يمكن تعديل المنطق في دالة `_generate_description`

## 🚀 طرق التشغيل

### التشغيل اليدوي
```bash
# تشغيل مرة واحدة
python main.py

# تشغيل مع تفاصيل إضافية
python main.py --verbose

# تشغيل تجريبي (بدون نشر)
python main.py --dry-run
```

### التشغيل المجدول
```bash
# بدء المجدول اليومي
python cli.py schedule

# تشغيل فوري ثم مجدول
python cli.py schedule --run-now

# إيقاف المجدول
Ctrl + C
```

### اختبار النظام
```bash
# اختبار جميع المكونات
python cli.py test

# اختبار مكون واحد
python test_components.py

# عرض حالة النظام
python cli.py status
```

## 🔧 إعدادات متقدمة

### تخصيص كلمات البحث للتصنيفات
**الموقع**: `src/content_generator.py` (السطر 175-182)
```python
category_keywords = {
    'تقنية': ['تقنية', 'تكنولوجيا', 'ذكي', 'رقمي'],
    'رياضة': ['رياضة', 'كرة', 'مباراة', 'بطولة'],
    # أضف كلمات مفتاحية جديدة
}
```

### تخصيص مقدمات المقالات
**الموقع**: `src/content_generator.py` (السطر 106-110)
```python
intros = [
    f"يشهد موضوع {topic['title']} اهتماماً متزايداً...",
    # أضف مقدمات جديدة هنا
]
```

### تخصيص خاتمات المقالات
**الموقع**: `src/content_generator.py` (السطر 146-150)
```python
conclusions = [
    f"في الختام، يبقى موضوع {topic['title']} محل اهتمام...",
    # أضف خاتمات جديدة هنا
]
```

## 📊 مراقبة النظام

### ملفات السجلات
```bash
# عرض آخر السجلات
tail -f logs/auto_blogger.log

# البحث في السجلات
grep "ERROR" logs/auto_blogger.log
```

### فحص حالة المدونة
```bash
python -c "
from src.blogger_publisher import BloggerPublisher
publisher = BloggerPublisher()
info = publisher.get_blog_info()
print(f'المدونة: {info[\"name\"]}')
print(f'عدد المقالات: {info[\"posts_count\"]}')
"
```

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة وحلولها

**1. خطأ في OAuth**:
```bash
# حذف ملفات المصادقة وإعادة المحاولة
rm token.json credentials.json
python cli.py test
```

**2. خطأ في RSS**:
```bash
# اختبار روابط RSS
python -c "
from src.trend_analyzer import TrendAnalyzer
analyzer = TrendAnalyzer()
topics = analyzer.get_trending_topics()
print(f'تم العثور على {len(topics)} موضوع')
"
```

**3. خطأ في الصور**:
```bash
# اختبار مفتاح Unsplash
python -c "
import os
print('مفتاح Unsplash:', os.getenv('UNSPLASH_ACCESS_KEY', 'غير محدد'))
"
```

## 📝 ملاحظات مهمة

1. **النسخ الاحتياطي**: احتفظ بنسخة من ملف `.env` في مكان آمن
2. **الأمان**: لا تشارك ملف `.env` أو تحمله على GitHub
3. **التحديثات**: راجع هذا الدليل بعد أي تحديثات للنظام
4. **الدعم**: استخدم `python cli.py status` لفحص حالة النظام

## 🎯 نصائح للاستخدام الأمثل

- **اختبر دائماً** قبل التشغيل الفعلي: `python cli.py test`
- **راقب السجلات** لمتابعة أداء النظام
- **حدّث RSS feeds** بانتظام لمحتوى متنوع
- **اضبط التوقيت** حسب جمهورك المستهدف
- **استخدم صور Unsplash** لجودة أفضل

---
*تم إنشاء هذا الدليل بواسطة Auto Blogger Devin*
