import pytest
import tempfile
import time
from messagio.message_center import MessageCenter
from .events import (
    EventTesterTmpFile,
    EventTester,
    NonDataclassMessagio,
)
from .listeners import (
    sub_tempfile_func,
)


def name_becomes_value(e: EventTester):
    e.name = "%s becomes %s" % (e.name, e.value)


@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
def test_event_pub_sub_async_file():
    value = "bar"
    tf, fname = tempfile.mkstemp()
    evt = EventTesterTmpFile(fname=fname, value=value)
    MessageCenter.singleton().subscribe(type(evt), sub_tempfile_func)
    MessageCenter.send(evt, sync=False)
    time.sleep(0.1)
    with open(fname, "r") as f:
        assert f.readline() == value


@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
def test_event_pub_sub_async_file_not_dataclass():
    value = "bar"
    tf, fname = tempfile.mkstemp()
    evt = NonDataclassMessagio(fname=fname, value=value)
    MessageCenter.singleton().subscribe(type(evt), sub_tempfile_func)
    MessageCenter.send(evt, sync=False)
    time.sleep(0.1)
    with open(fname, "r") as f:
        assert f.readline() == value


def test_event_pub_sub_sync():
    value = "bar"
    name = "foo"
    evt = EventTester(name=name, value=value)
    MessageCenter.singleton().subscribe(EventTester, name_becomes_value)
    assert evt.name == name
    MessageCenter.send(evt, sync=True)
    assert evt.name == "%s becomes %s" % (name, value)

    MessageCenter.singleton().unsubscribe(EventTester, name_becomes_value)
    evt = EventTester(name=value, value=name)
    MessageCenter.send(evt, sync=True)
    assert evt.name == value
