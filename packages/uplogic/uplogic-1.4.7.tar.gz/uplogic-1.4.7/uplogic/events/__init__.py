'''TODO: Documentation
'''

from bge import logic
import time


def get_event_manager():
    scene = logic.getCurrentScene()
    if ULEventManager.update not in scene.post_draw:
        scene.post_draw.append(ULEventManager.update)
        # ULEventManager.initialized = True


class ULEventManager():
    '''TODO: Documentation
    '''
    events = {}
    callbacks = []
    initialized = False
    done = []

    @classmethod
    def update(cls):
        for cb in cls.callbacks.copy():
            cb()

    @classmethod
    def log(cls):
        if cls.events:
            print('Events:')
            for evt in cls.events:
                print(f'\t{evt}:\t{cls.events[evt].content}')


    @classmethod
    def schedule(cls, cb):
        if not cls.initialized:
            get_event_manager()
        cls.callbacks.append(cb)

    @classmethod
    def deschedule(cls, cb):
        if not cls.initialized:
            get_event_manager()
        cls.callbacks.remove(cb)

    @classmethod
    def register(cls, event):
        if not cls.initialized:
            get_event_manager()
        cls.events[event.name] = event
        cls.schedule(event.remove)

    @classmethod
    def send(cls, name, content, messenger) -> None:
        if not cls.initialized:
            get_event_manager()
        ULEvent(name, content, messenger)


    @classmethod
    def receive(cls, name):
        if not cls.initialized:
            get_event_manager()
        return cls.events.get(name, None)

    @classmethod
    def consume(cls, name):
        if not cls.initialized:
            get_event_manager()
        return cls.events.pop(name, None)


class ULEvent():
    '''TODO: Documentation
    '''

    def __init__(self, name, content=None, messenger=None):
        self.name = name
        self.content = content
        self.messenger = messenger
        ULEventManager.schedule(self.register)

    def register(self):
        ULEventManager.register(self)
        ULEventManager.deschedule(self.register)

    def remove(self):
        ULEventManager.events.pop(self.name, None)
        ULEventManager.deschedule(self.remove)


def send(name: str, content=None, messenger=None) -> None:
    '''TODO: Documentation
    '''
    ULEventManager.send(name, content, messenger)


def receive(name: str) -> ULEvent:
    '''TODO: Documentation
    '''
    return ULEventManager.receive(name)


def consume(name: str):
    '''TODO: Documentation
    '''
    return ULEventManager.consume(name, None)


def schedule(name: str, content=None, messenger=None, delay=0.0):
    '''TODO: Documentation
    '''
    ScheduledEvent(delay, name, content, messenger)


class ScheduledEvent():
    '''TODO: Documentation
    '''

    def __init__(self, delay, name, content, messenger):
        self.time = time.time()
        self.delay = self.time + delay
        self.name = name
        self.content = content
        self.messenger = messenger
        ULEventManager.schedule(self.send_scheduled)

    def send_scheduled(self):
        if time.time() >= self.delay:
            ULEventManager.deschedule(self.send_scheduled)
            ULEvent(self.name, self.content, self.messenger)


def schedule_callback(cb, delay=0.0, arg=None):
    '''TODO: Documentation
    '''
    ScheduledCallback(cb, delay, arg)


class ScheduledCallback():
    '''TODO: Documentation
    '''
    delay: float = 0
    arg = None
    callback = None

    def __init__(self, cb, delay=0.0, arg=None):
        ULEventManager.schedule(self.call_scheduled)
        self.time = time.time()
        self.delay = self.time + delay
        self.callback = cb
        self.arg = arg

    def call_scheduled(self):
        if time.time() >= self.delay:
            if self.arg is not None:
                self.callback(self.arg)
            else:
                self.callback()
            ULEventManager.deschedule(self.call_scheduled)
