from datetime import datetime

from app.device.services.device import DeviceService
from celery import shared_task


@shared_task
def change_device_automated_task_to_undone():
    result = DeviceService.change_device_automated_task_to_undone()
    return f"Changed {result} device automated tasks to undone."


@shared_task
def check_invockable_device_automated_task():
    rounded_datetime = datetime.now().replace(second=0, microsecond=0)
    result = DeviceService.check_invockable_device_automated_task(rounded_datetime)
    return f"Result of invoked tasks: {result}"


@shared_task
def clear_device_automated_task_no_reocurring():
    result = DeviceService.clear_device_automated_task_no_reocurring()
    return f"Deleted {result} device automated tasks that are not recurring."
