#! /usr/bin/python
import argparse

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
Gets life expectency from the Social Security Administration's website.
""")
parser.add_argument('sex', help='gender', choices=['m', 'f'])
parser.add_argument('dob', help='date of birth (MM/DD/YYYY)')
parser.add_argument('-v', '--version', action="version",
                    version=f"{get_version()}",
                    help='display version number')
kwargs = vars(parser.parse_args())
main = Main(**kwargs)
main.run()
