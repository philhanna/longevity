from longevity.parser import State


class InitState(State):

    def __init__(self):
        super().__init__(__class__.__name__)
