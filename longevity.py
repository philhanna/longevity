#! /usr/bin/python
import argparse
import sys
from datetime import date

from longevity import Main


def get_version():
    import subprocess, re
    version = None
    cp = subprocess.run(['pip', 'show', 'longevity'], capture_output=True, text=True)
    if cp.returncode == 0:
        output = cp.stdout
        for token in output.split('\n'):
            m = re.match(r'^Version: (.*)', token)
            if m:
                version = m.group(1)
                break
    return version


parser = argparse.ArgumentParser(description="""
Gets life expectancy from the Social Security Administration's website.
""")
parser.add_argument('sex', help='gender', choices=['m', 'f'])
parser.add_argument('dob', help='date of birth (yyyy-mm-dd)')
parser.add_argument('-v', '--version', action="version",
                    version=f"version={get_version()}",
                    help='displays version number and exit')
parser.add_argument('-j', '--json_output', action="store_true", help="Sends JSON output to stdout")
kwargs = vars(parser.parse_args())
try:
    main = Main(**kwargs)
    result = main.run()
    if kwargs["json_output"]:
        print(result.get_json_output())
    else:
        print(f"current age      = {result.current_age}")
        print(f"additional years = {result.additional_years}")
        print(f"total years      = {result.total_years}")
        print(f"expiration date  = {date.isoformat(result.death_date)}")
except ValueError as ex:
    print(ex, file=sys.stderr)
