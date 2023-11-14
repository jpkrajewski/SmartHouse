from celery import Celery
from celery.schedules import crontab
from core.config import config

app = Celery("smart_house_automation")

app.conf.update(
    broker_url=config.CELERY_BROKER_URL,
    result_backend=config.CELERY_BACKEND_URL,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Warsaw",
    enable_utc=True,
    include=["celery_task.tasks"],
)

app.conf.beat_schedule = {
    "change-device-automated-task-to-undone": {
        "task": "celery_task.tasks.change_device_automated_task_to_undone",
        "schedule": crontab(minute=0, hour=0),
    },
    "check-invokeable-device-automated-task": {
        "task": "celery_task.tasks.check_invockable_device_automated_task",
        "schedule": crontab(minute="*/1"),
    },
    "clear-device-automated-task-no-reocurring": {
        "task": "celery_task.tasks.clear_device_automated_task_no_reocurring",
        "schedule": crontab(minute=0, hour=0),
    },
}
