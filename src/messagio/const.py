from enum import IntEnum, unique


class Messagio:
    @classmethod
    def get_name(cls):
        return "%s.%s" % (cls.__module__, cls.__name__)

    def fire(self, sync=False) -> None:
        """
        Send the messagio via message center.
        :param sync: send synchronously, default False
        """
        from .message_center import MessageCenter

        MessageCenter.send(messagio=self, sync=sync)


@unique
class TASK_PRIORITY(IntEnum):
    LOW = 0
    LESS = 3
    REGULAR = 5
    MORE = 7
    HIGH = 9
    EPIC = 10
