import re
from enum import Enum


class States(Enum):
    INIT = 1
    AFTER_TABLE_START = 2
    AFTER_FIRST_TR_START = 3
    AFTER_FIRST_TR_END = 4
    AFTER_READING_CURRENT_AGE = 5


class ResponseParser:
    """ Parses the HTML returned by the SSA web site """

    def __init__(self, html: str):
        """ Given the response HTML, returns the parsed values """
        state = States.INIT
        with open(html) as fp:
            for line in fp:
                line = line.strip()

                if state == States.INIT:
                    m = re.match(r'<table.*summary="life expectancy table"', line)
                    if m:
                        state = States.AFTER_TABLE_START

                elif state == States.AFTER_TABLE_START:
                    m = re.match(r'<tr', line)
                    if m:
                        state = States.AFTER_FIRST_TR_START

                elif state == States.AFTER_FIRST_TR_START:
                    m = re.match(r'</tr')
                    if m:
                        state = States.AFTER_FIRST_TR_END

                elif state == States.AFTER_FIRST_TR_END:
                    m = re.search(r'<td[^>]*>([^<]+)<')
                    if m:
                        state = States.AFTER_READING_CURRENT_AGE
                        current_age = m.group(1)
