from datetime import date

SSI_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"


def get_date_fields(dob: date):
    """ Extracts date fields and formats them in the way the
    cgi program expects them."""
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
