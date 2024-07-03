# modules/event_system.py

from typing import Callable, Dict, List

class EventSystem:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def publish(self, event_name: str, *args, **kwargs):
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback(*args, **kwargs)

event_system = EventSystem()