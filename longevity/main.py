from datetime import datetime

from longevity import Requester


class Main:
    """Mainline for running the calculator"""

    def __init__(self, **kwargs):
        self._sex = kwargs["sex"]
        dobstr = kwargs["dob"]
        dob = datetime.strptime(dobstr, "%m/%d/%Y")
        self._dob = dob.date()

    @property
    def sex(self):
        return self._sex

    @property
    def dob(self):
        return self._dob

    def run(self):
        """Runs the calculator"""
        return Requester(self.sex, self.dob)
