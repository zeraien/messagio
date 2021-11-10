import logging

logger = logging.getLogger("messagio")
try:
    import importlib
    import os
    from os.path import basename

    from django.apps import apps

    def _yield_file(app_path):
        try:
            with os.scandir(app_path) as it:
                for entry in it:
                    if entry.name == "messagio.py":
                        yield entry.name[:-3]
                    elif entry.name == "tasks.py":
                        yield entry.name[:-3]
                    elif entry.name == "messagio":
                        yield entry.name
        except FileNotFoundError:
            pass

    def autodiscover_listeners():

        for app_config in list(apps.app_configs.values()):
            app_name = app_config.name

            try:
                app_path = app_config.path
                for f in _yield_file(app_path):
                    logger.debug(
                        "Importing messagio listeners from %s.%s" % (app_name, f)
                    )
                    importlib.import_module("%s.%s" % (app_name, f))
            except AttributeError as e:
                logger.exception(e)


except ImportError:
    logger.exception(
        "Django is not installed so autodiscover can not be used.", exc_info=True
    )
