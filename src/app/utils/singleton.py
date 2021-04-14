import threading


class SingletonMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instance = None
        cls._locker = threading.Lock()

    @property
    def instance(self, *args, **kwargs):
        if self._instance is None:
            with self._locker:
                if self._instance is None:
                    self._instance = self(*args, **kwargs)
        return self._instance