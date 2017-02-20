from boundaries import *
import pytz
from datetime import datetime
import random
from django.contrib.gis.geos import Point, GEOSGeometry


def get_timezone_by_country_name(country):

    """This function takes the name of a country object, gets the two letter abbreviation
    from GADM and returns the appropriate timezone from pytz or UTC."""

    try:
        two_letters = country.iso2.lower()

    except Exception:
        return pytz.utc

    timezones = pytz.country_timezones[two_letters]

    return pytz.timezone(timezones[0]) if timezones else pytz.utc

def generate_random_points(bounding_box):
    yield Point(
        x=random.uniform(bounding_box[0], bounding_box[2]),
        y=random.uniform(bounding_box[1], bounding_box[2])
    )





