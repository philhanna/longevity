class State:
    """ Abstract base class for all parsing states """
    def __init__(self, name):
        self._name = name
        pass

    @property
    def name(self):
        return self._name

    def handleLine(self, line: str) -> 'State':
        raise RuntimeError('Subclasses must implement handleLine()')
