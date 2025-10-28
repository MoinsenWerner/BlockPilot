from celery import Celery

from .config import settings

celery_app = Celery(
    "panel",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task
def run_scheduled_backup(instance_id: int) -> str:
    return f"Scheduled backup executed for instance {instance_id}"


@celery_app.task
def run_health_check(instance_id: int) -> str:
    return f"Health check executed for instance {instance_id}"
