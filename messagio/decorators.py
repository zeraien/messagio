import typing
from dataclasses import dataclass

from .const import Messagio, TASK_PRIORITY


def messagio_dataclass(cls=None, /):
    def wrap(_cls):
        return dataclass(init=True, eq=True)(_cls)

    # See if we're being called as @dataclass or @dataclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)


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
            print("Registering task %s/%s" % (messagio, func))
            MessageCenter.singleton().subscribe(
                event_type=messagio, func=func, **task_args
            )
        return func

    return deco
