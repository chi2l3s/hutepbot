from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from tasks.notifications import check_expiring_subscriptions

scheduler = AsyncIOScheduler()

def setup_scheduler(bot: Bot):
    scheduler.add_job(
        check_expiring_subscriptions,
        CronTrigger(hour=10, minute=0),
        kwargs={'bot': bot}
    )
    scheduler.start()