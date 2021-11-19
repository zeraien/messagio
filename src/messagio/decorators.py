import logging
import typing

from .const import Messagio, TASK_PRIORITY

logger = logging.getLogger("messagio")


def listen_to_message(
    *messagios: type(Messagio),
    priority=TASK_PRIORITY.REGULAR,
    autoretry_for=tuple(),
    max_retries=None,
    default_retry_delay=None,
):
    """
    A function decorated with this decorator will be called whenever any
    event of the provided types is "fired".
    The function can be retried if it raises an exception the first time.

    :param messagios: the event types to listen to
    :param priority: priority of the task, relevant to queue managers
    :param autoretry_for: list of exceptions that allow this to auto-retry
    :param max_retries: max number of times to retry the function call
    :param default_retry_delay: how many seconds to wait before retrying
    """

    def deco(func: typing.Callable[[Messagio], None]):

        ####################################################
        # not sure if we should get to the "bottom" of this
        while hasattr(func, "__wrapped__"):
            func = func.__wrapped__
        ####################################################

        task_args = dict(
            priority=priority,
            autoretry_for=autoretry_for,
            max_retries=max_retries,
            default_retry_delay=default_retry_delay,
        )
        from .message_center import MessageCenter

        for messagio in messagios:
            logger.debug("Registering task %s/%s", messagio, func)
            MessageCenter.singleton().subscribe(
                event_type=messagio, func=func, **task_args
            )
        return func

    return deco
