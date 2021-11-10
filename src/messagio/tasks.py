from celery import shared_task
from . import Messagio


@shared_task
def message_runner(func, messagio: Messagio):
    func(messagio)
