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

### التشغيل المجدول (موصى به)
```bash
# تشغيل المجدول اليومي في 9 مساء بتوقيت السعودية
python cli.py schedule

# تشغيل فوري ثم مجدول
python cli.py schedule --run-now
```

### استخدام Crontab (بديل)
```bash
# إضافة إلى crontab للتشغيل اليومي في 9 مساء بتوقيت السعودية
0 18 * * * cd /path/to/auto-blogger-devin && /usr/bin/python3 main.py
```

### التحكم في التوقيت
عدّل `SCHEDULE_TIME` في ملف `.env`:
```env
SCHEDULE_TIME=18:00  # 9 مساء بتوقيت السعودية
```
