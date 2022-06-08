class State:
    """ Abstract base class for all parsing states """
    def __init__(self, cls):
        self._name = cls.__name__
        pass

    @property
    def name(self):
        return self._name

    def handleLine(self, line: str) -> 'State':
        raise RuntimeError('Subclasses must implement handleLine()')
