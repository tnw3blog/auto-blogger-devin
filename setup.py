#!/usr/bin/env python3
"""
Setup script for Auto Blogger Devin
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """إنشاء ملف .env إذا لم يكن موجوداً"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 إنشاء ملف .env...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ تم إنشاء ملف .env")
        print("⚠️ يرجى تحديث المتغيرات في ملف .env قبل التشغيل")
    else:
        print("✅ ملف .env موجود")

def check_requirements():
    """التحقق من المتطلبات"""
    try:
        import requests
        import feedparser
        import pytrends
        from google.auth.transport.requests import Request
        print("✅ جميع المتطلبات مثبتة")
        return True
    except ImportError as e:
        print(f"❌ متطلب مفقود: {e}")
        print("يرجى تشغيل: pip install -r requirements.txt")
        return False

def setup_logging_directory():
    """إنشاء مجلد السجلات"""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✅ تم إنشاء مجلد السجلات")

def main():
    print("🚀 إعداد Auto Blogger Devin...")
    
    if sys.version_info < (3, 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        sys.exit(1)
    
    create_env_file()
    setup_logging_directory()
    
    if not check_requirements():
        sys.exit(1)
    
    print("\n✅ تم إكمال الإعداد بنجاح!")
    print("\nالخطوات التالية:")
    print("1. قم بتحديث ملف .env بالمعلومات المطلوبة")
    print("2. قم بإعداد Blogger API credentials")
    print("3. شغل البرنامج: python main.py")
    print("\nللمساعدة، راجع ملف README.md")

if __name__ == "__main__":
    main()
