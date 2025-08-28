"""
EventBus simples baseado em listas de callbacks (sincrono para demo).
"""
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, fn: Callable):
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload):
        for fn in self._subs.get(topic, []):
            fn(payload)
