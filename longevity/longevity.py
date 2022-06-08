from datetime import date


def split_date(dob: date):
    monthofbirth = f"{dob.month - 1}"
    dayofbirth = f"{dob.day:02d}"
    yearofbirth = f"{dob.year}"
    return monthofbirth, dayofbirth, yearofbirth


def get_longevity(sex: str, dob: date):
    monthofbirth, dayofbirth, yearofbirth = split_date(dob)
