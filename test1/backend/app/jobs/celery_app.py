from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "amazon_ads",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "data-sync-hourly": {
            "task": "app.jobs.tasks.sync_ad_data",
            "schedule": 3600.0,
        },
        "bidding-strategy": {
            "task": "app.jobs.tasks.execute_bidding_strategy",
            "schedule": 14400.0,
        },
        "keyword-mining": {
            "task": "app.jobs.tasks.mine_keywords",
            "schedule": 86400.0,
        },
    },
)
