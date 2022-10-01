SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"

__all__ = [
    'SSA_URL',
    'ResponseParser',
    'Requester',
]

from .response_parser import ResponseParser
from .requester import Requester
