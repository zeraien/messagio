import logging

from .events import EventTester, EventTesterTmpFile
from decorators import listen_to_message

logger = logging.getLogger("messagio")


@listen_to_message(EventTester)
def debug_task(e: EventTester):
    logger.debug("DEBUG TASK IS RUNNING PROPERLY WITH EVENT: %s" % e)
    print("print() DEBUG TASK IS RUNNING PROPERLY WITH EVENT: %s" % e)


def sub_tempfile_func(e: EventTesterTmpFile) -> None:
    """writes a value to a file based on the contents of the event"""
    print("Writing to temp file...")
    with open(e.fname, "w") as f:
        f.write(e.value)


def sub_func(e: EventTester):
    e.name = e.value
