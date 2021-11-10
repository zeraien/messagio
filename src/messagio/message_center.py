import logging
from collections import defaultdict

import celery

from .abstract_message_center import AbstractMessageCenter
from .const import Messagio, TASK_PRIORITY

logger = logging.getLogger("odb_ecs")


class MessageCenter(AbstractMessageCenter):
    def __init__(self):
        self._task_settings = defaultdict(dict)
        self._subs = defaultdict(set)

    @classmethod
    def send(cls, messagio, sync=False):
        """
        send a message to all who would listen.

        :param messagio: message type as a string or Enum
        :param sync: send message synchronously
        """
        logger.debug("[PUB] Publishing message %s: %s" % (messagio.get_name(), messagio))
        cls.singleton().send_message(messagio, sync=sync)

    def get_subscribers(self, message_type: Messagio):
        return list(self._subs[message_type.get_name()])

    def unsubscribe(
        self,
        event_type,
        func,
    ):
        logger.debug(
            "[UNSUB] Handler %(func)s unsub from %(name)s"
            % {"func": func, "name": event_type.get_name()}
        )
        if event_type.get_name() in self._task_settings:
            del self._task_settings[event_type.get_name()]
        if event_type.get_name() in self._subs:
            self._subs[event_type.get_name()].remove(func)

    def subscribe(
        self,
        event_type,
        func,
        priority=TASK_PRIORITY.REGULAR,
        autoretry_for=tuple(),
        max_retries=None,
        default_retry_delay=None,
    ):
        logger.debug(
            "[SUB] Handler %(func)s sub to %(name)s"
            % {"func": func, "name": event_type.get_name()}
        )
        self._task_settings[event_type.get_name()] = dict(
            priority=priority,
            autoretry_for=autoretry_for,
            max_retries=max_retries,
            default_retry_delay=default_retry_delay,
        )
        self._subs[event_type.get_name()].add(func)

    def send_message(self, event: Messagio, sync: bool = False):
        from .tasks import message_runner

        subscribers = self.get_subscribers(event)

        extra_task_settings = dict(
            # todo allow for using a different routing key
            # routing_key=settings.ECS_MESSAGE_QUEUE, queue=settings.ECS_MESSAGE_QUEUE
        )
        extra_task_settings.update(self._task_settings.get(event.get_name(), {}))

        for func in subscribers:
            if not sync:
                message_runner.apply_async(
                    kwargs=dict(
                        func=func,
                        messagio=event,
                    ),
                    serializer="pickle",
                    **extra_task_settings
                )
            else:
                message_runner.apply(
                    kwargs=dict(
                        func=func,
                        messagio=event,
                    ),
                    serializer="pickle",
                )
