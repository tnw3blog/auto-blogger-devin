"""
Daily Scheduler - جدولة التشغيل اليومي
"""

import logging
import schedule
import time
from datetime import datetime
import config

logger = logging.getLogger(__name__)

class DailyScheduler:
    def __init__(self, main_function):
        self.main_function = main_function
        
    def setup_daily_schedule(self):
        """إعداد الجدولة اليومية"""
        schedule.every().day.at(config.DAILY_RUN_TIME).do(self._run_with_logging)
        logger.info(f"✅ تم إعداد الجدولة اليومية في {config.DAILY_RUN_TIME}")
    
    def _run_with_logging(self):
        """تشغيل المهمة مع التسجيل"""
        logger.info(f"🕐 بدء التشغيل المجدول في {datetime.now()}")
        try:
            self.main_function()
            logger.info("✅ تم إكمال التشغيل المجدول بنجاح")
        except Exception as e:
            logger.error(f"❌ خطأ في التشغيل المجدول: {str(e)}")
    
    def run_scheduler(self):
        """تشغيل المجدول"""
        logger.info("🚀 بدء تشغيل المجدول...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_once_now(self):
        """تشغيل فوري لمرة واحدة"""
        logger.info("▶️ تشغيل فوري...")
        self._run_with_logging()
