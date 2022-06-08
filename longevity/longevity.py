from datetime import date

SSI_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"


def get_date_fields(dob: date):
    """ Extracts date fields and formats them in the way the
    cgi program expects them:

    - monthofbirth is the month field minus 1 (0-11)
    - dayofbirth is the day field with leading zero if less than 10
    - yearofbirth is a 4-digit year field

    These fields are returned as tuple of 3 strings
    """
    monthofbirth = f"{dob.month - 1}"
    dayofbirth = f"{dob.day:02d}"
    yearofbirth = f"{dob.year}"
    return monthofbirth, dayofbirth, yearofbirth


def format_post_data(sex: str, dob: date) -> dict :
    mm, dd, yyyy = get_date_fields(dob)
    postdata = {
        "sex": sex,
        "monthofbirth": mm,
        "dayofbirth": dd,
        "yearofbirth": yyyy,
    }
    return postdata


def get_longevity(sex: str, dob: date):
    postdata = format_post_data(sex, dob)
