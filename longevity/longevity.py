from datetime import date


def split_date(dob: date):
    """ Extracts date fields and formats them the way the
    cgi program expects them."""
    monthofbirth = f"{dob.month - 1}"
    dayofbirth = f"{dob.day:02d}"
    yearofbirth = f"{dob.year}"
    return monthofbirth, dayofbirth, yearofbirth


def get_longevity(sex: str, dob: date):
    monthofbirth, dayofbirth, yearofbirth = split_date(dob)
