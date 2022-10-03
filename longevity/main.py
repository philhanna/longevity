from datetime import date

from longevity import Requester


class Main:
    """Mainline for running the calculator"""

    def __init__(self, **kwargs):
        self._sex = kwargs["sex"]
        self._dob = date.fromisoformat(kwargs["dob"])

    @property
    def sex(self) -> str:
        """Returns the sex input parameter"""
        return self._sex

    @property
    def dob(self) -> date:
        return self._dob

    def run(self) -> Requester:
        """Runs the calculator"""
        return Requester(self.sex, self.dob)
