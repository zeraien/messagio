try:
    import importlib
    import logging
    import os
    from os.path import basename

    from django.apps import apps

    logger = logging.getLogger("messagio")

    def _yield_file(app_path):
        try:
            with os.scandir(app_path) as it:
                for entry in it:
                    if entry.name == "messagio.py":
                        yield entry.name[:-3]
                    elif entry.name == "messagio":
                        yield entry.name
                    elif entry.name == "messagio/listeners.py":
                        yield entry.name[:-3].replace("/", ".")
        except FileNotFoundError:
            pass

    def autodiscover_listeners():

        for app_config in list(apps.app_configs.values()):
            app_name = app_config.name

            try:
                app_path = app_config.path
                for f in _yield_file(app_path):
                    logger.debug("Importing tasks from %s.%s" % (basename(app_path), f))
                    importlib.import_module("%s.%s" % (app_name, "tasks"))
            except AttributeError as e:
                logger.exception(e)


except ImportError:
    print("Django is not installed so autodiscover can not be used.")