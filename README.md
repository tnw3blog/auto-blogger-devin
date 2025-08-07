# Auto Blogger Devin

سكربت Python مجاني بالكامل للنشر التلقائي على منصة Blogger

## الميزات
- البحث عن الأخبار الأكثر تداولاً من Google Trends و RSS feeds
- إعادة صياغة المحتوى تلقائياً
- تنسيق HTML احترافي
- إضافة الصور المناسبة
- تصنيفات تلقائية
- وصف البحث المحسن
- النشر التلقائي على Blogger
- جدولة يومية

## متطلبات التشغيل
- Python 3.8+
- حساب Google مع تفعيل Blogger API
- اتصال بالإنترنت

## التثبيت والإعداد
```bash
pip install -r requirements.txt
python setup.py
```

## الاستخدام
```bash
python main.py
```

## الجدولة اليومية
```bash
# إضافة إلى crontab للتشغيل اليومي
0 9 * * * /usr/bin/python3 /path/to/auto-blogger-devin/main.py
```
