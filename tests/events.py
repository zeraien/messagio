import logging
from dataclasses import dataclass

from src.messagio import Messagio

logger = logging.getLogger("messagio")


@dataclass
class EventTester(Messagio):
    name: str
    value: str


@dataclass
class EventTesterTmpFile(Messagio):
    fname: str
    value: str


class NonDataclassMessagio(Messagio):
    def __init__(self, fname: str, value: str):
        self.fname = fname
        self.value = value
