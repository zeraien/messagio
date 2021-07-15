# Welcome to Messagio

It's sort of like *pubsub*, but evolved.

Messagio works out of the box with **Django** and **Celery**.

You can define events, aka messagios, with specific payloads, the messagios themselves are preferably
python dataclasses, and their payloads are pickled, but you can in theory use any class as a messagio.

Now you can subscribe any function to listen for those events and do stuff when
an event is received.

Any number of functions can subscribe to a single event.
Every function can subscribe to one or more events.
The events are transmitted using celery, so make sure you configure

# Celery Config

As long as celery is configured in your django setup, you don't need to do anything.
However, it might be wise to have a custom queue for your messagio events, to make sure they get the priority they deserve.

In django you can configure it as such in django `settings.py` or your celery settings:
```python3
CELERY_TASK_ROUTES = (
    [
        ('messagio.tasks.*', {'queue': 'messagio'}),
    ],
)
```

# Defining Messagios

A messagio is a class that can be pickled, and extends from the `Messagio` class.
The best way to create messagios is with `dataclasses`, so you can decorate your class with `@messagio` which will turn that class into a dataclass.
Your messagio class needs to extend `Messagio`, the `@messagio` decorator is optional however.

Here are two ways to define messagios:
```python3
@messagio
class PerformAction(Messagio):
   action_name:str
   obj:any

class ActionPerformed(Messagio):
   def __init__(action_name:str,obj:any):
       self.action_name=action_name
       self.obj = obj

```

# Publishing messagios

Publishing messagios is simple, just `fire` it.
```python3
obj = Model.objects.get(pk=123)
PerformAction("foo_action", obj).fire()
```

Fire accepts certain additional parameters:
- `sync:bool` will call the messagio synchronously without going through celery (uses `celery.task.apply`)

# Listening to messagios

Any function can be configured as a listener.
A listener can listen to one or more messagio types and will receive the messagio object itself as the first and only parameter.

The subsciption can come with some extra arguments, these are all passed directly to celery.

- `priority: TASK_PRIORITY` set a priority that will be passed to celery, if your celery does not use priorities, this is ignored. The priorities are integers and depend on your celery configuration, some default options are available in `const.py`
- `autoretry_for: tuple[Exception]` a list of exceptions that trigger an auto-retry, again passed to celery
- `max_retries: int`  number of times to auto retry if auto retry is enabled, default is no auto retry
- `default_retry_delay: float` how long to wait before auto retrying


```python3
# high priority listener
@listen_to_message(PerformAction, priority=10)
def high_prio_listener(messagio:PerformAction):
    # do something with your messagio
    pass

@listen_to_message(PerformAction, ActionPerformed)
def listener_of_many(messagio:typing.Union[PerformAction, ActionPerformed]):
    # do something with your messagio
    pass

# low priority listener
@listen_to_message(PerformAction, priority=1)
def log_me(messagio:PerformAction):
    logging.getLogger("foo").info("Action was performed %s" % messagio.action_name)

```

Messagio functions will be executed by your celery worker and they are executed sequentially in the order that they were subscribed.
A single published messagio will be executed by a single worker and a messagio can be published as many times as you want.

You can also subscribe directly using the message center
```python3
def any_func(msg:PerformAction):
    #do stuff
    pass

MessageCenter.singleton().subscribe(PerformAction, any_function)
```

# Abstract message center?
If you want, you can roll your own message center that does not use celery to transport messages, for example if you want to use a daemon or some other transport protocol like huey.
