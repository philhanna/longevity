SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"

__all__ = [
    'SSA_URL',
    'ResponseParser',
    'Requester',
    'Main',
]

from .response_parser import ResponseParser
from .requester import Requester
from .main import Main
