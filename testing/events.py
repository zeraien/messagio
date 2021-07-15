import logging

from messagio import Messagio, messagio_dataclass

logger = logging.getLogger("messagio")


@messagio_dataclass
class EventTester(Messagio):
    name: str
    value: str


@messagio_dataclass
class EventTesterTmpFile(Messagio):
    fname: str
    value: str


class NonDataclassMessagio(Messagio):
    def __init__(self, fname: str, value: str):
        self.fname = fname
        self.value = value
