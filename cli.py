#!/usr/bin/env python3
"""
Command Line Interface for Auto Blogger Devin
"""

import argparse
import logging
import sys
from datetime import datetime

from main import main as run_main
from test_components import main as run_tests
from src.scheduler import DailyScheduler
from src.blogger_publisher import BloggerPublisher

def setup_logging(verbose=False):
    """إعداد نظام التسجيل"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def cmd_run(args):
    """تشغيل البرنامج مرة واحدة"""
    print("🚀 تشغيل Auto Blogger Devin...")
    run_main()

def cmd_test(args):
    """اختبار المكونات"""
    print("🧪 اختبار مكونات النظام...")
    run_tests()

def cmd_schedule(args):
    """تشغيل المجدول"""
    print("⏰ بدء تشغيل المجدول اليومي...")
    scheduler = DailyScheduler(run_main)
    scheduler.setup_daily_schedule()
    
    if args.run_now:
        scheduler.run_once_now()
    
    scheduler.run_scheduler()

def cmd_status(args):
    """عرض حالة النظام"""
    print("📊 فحص حالة النظام...")
    
    try:
        publisher = BloggerPublisher()
        blog_info = publisher.get_blog_info()
        
        if blog_info:
            print(f"✅ متصل بالمدونة: {blog_info['name']}")
            print(f"📝 عدد المنشورات: {blog_info['posts_count']}")
            print(f"🔗 الرابط: {blog_info['url']}")
        else:
            print("❌ غير متصل بـ Blogger")
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {str(e)}")

def main():
    """الواجهة الرئيسية لسطر الأوامر"""
    parser = argparse.ArgumentParser(
        description='Auto Blogger Devin - مولد المحتوى التلقائي للمدونات',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  %(prog)s run                    # تشغيل مرة واحدة
  %(prog)s test                   # اختبار المكونات
  %(prog)s schedule               # تشغيل المجدول
  %(prog)s schedule --run-now     # تشغيل فوري ثم مجدول
  %(prog)s status                 # عرض الحالة
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='عرض تفاصيل أكثر')
    
    subparsers = parser.add_subparsers(dest='command', help='الأوامر المتاحة')
    
    run_parser = subparsers.add_parser('run', help='تشغيل البرنامج مرة واحدة')
    run_parser.set_defaults(func=cmd_run)
    
    test_parser = subparsers.add_parser('test', help='اختبار مكونات النظام')
    test_parser.set_defaults(func=cmd_test)
    
    schedule_parser = subparsers.add_parser('schedule', help='تشغيل المجدول اليومي')
    schedule_parser.add_argument('--run-now', action='store_true',
                                help='تشغيل فوري قبل بدء المجدول')
    schedule_parser.set_defaults(func=cmd_schedule)
    
    status_parser = subparsers.add_parser('status', help='عرض حالة النظام')
    status_parser.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    setup_logging(args.verbose)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البرنامج بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
