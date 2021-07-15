import pytest


@pytest.fixture(scope="session")
def celery_config():
    return dict(
        broker_url="redis://",
        result_backend="redis://",
        accept_content=["json", "pickle"],
        task_serializer="pickle",
    )
