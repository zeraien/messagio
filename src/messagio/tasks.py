from celery import shared_task


@shared_task
def message_runner(func, event: "ECSEvent"):
    func(event)
