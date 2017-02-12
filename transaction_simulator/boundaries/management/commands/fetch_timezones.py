# Imports

#Django Management Command Imports

from django.core.management.base import BaseCommand, CommandError


# Generic Python Library Imports

import sys, os
from zipfile import ZipFile

# Requests related things

import requests
from clint.textui import progress


# Useful Constants

BOUNDARIES_URL = 'http://efele.net/maps/tz/world/tz_world_mp.zip'

BOUNDARIES_SHAPEFILE = './shapefiles/tz_world_mp.shp.zip'

class Command(BaseCommand):
    args = ''
    help = 'Fetches the Natural Earth Timezones Shapefile'

    def handle(self, *args, **options):
        try:
            fetch_data()
            unzip_data()

        except Exception as ex:
            raise CommandError("There was an error at the command level: %s" % (ex))
            sys.exit()

        self.success = True

        # Output mesages

        if self.success == True:
            self.stdout.write('Successfully fetched the boundaries for Natural Earth Timezone boundaries.')

def fetch_data():

    """This function fetches the Natural Earth timezones shapefile."""

    print "Now fetching the timezones geodatabase."

    # variables for logic (magic strings/numbers)

    r = requests.get(BOUNDARIES_URL, stream = True)

    with open(BOUNDARIES_SHAPEFILE, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

def unzip_data():

    boundaries_shp_zip = ZipFile(BOUNDARIES_SHAPEFILE)
    boundaries_shp_zip.extractall()

