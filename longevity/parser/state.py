import re


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


class InitState(State):
    def __init__(self):
        super().__init__(__class__)
        self.regexp = re.compile(r'<table ... summary="life expectancy table"')

    def handleLine(self, line: str) -> 'State':
        next_state = self
        m = self.regexp.match(line)
        pass
