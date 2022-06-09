import unittest
import os.path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class MyTestCase(unittest.TestCase):

    def test_something(self):
        filename = os.path.abspath("long.html")
        with open(filename) as fp:
            soup = BeautifulSoup(fp, "html.parser")
            table = soup.table
            trs = [x for x in table.findAll("tr")]
            tr = trs[1]
            tds = [x for x in tr.findAll("td")]
            print(f"DEBUG: number of tds = {len(tds)}")
            for i, td in enumerate(tds):
                print(f"DEBUG: td.{i} = {td.contents[0]}")
