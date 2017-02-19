# Imports

#Django Management Command Imports

from django.core.management.base import BaseCommand, CommandError


# Generic Python Library Imports

import sys, os
from zipfile import ZipFile

# Requests related things

import requests
from clint.textui import progress


class Command(BaseCommand):
    args = ''
    help = 'Fetches the Global Adminstrative Boundaries Shapefile'

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
            self.stdout.write('Successfully fetched the boundaries for global administrative boundaries.')

def fetch_data():

    """This function fetches the GADB geodatabase."""

    print "Now fetching the boundaries geodatabase."

    # variables for logic (magic strings/numbers)

    boundaries_url = 'http://biogeo.ucdavis.edu/data/gadm2.8/gadm28_levels.shp.zip'

    boundaries_shapefile = './shapefiles/global_boundaries.shp.zip'

    boundaries_gdb_url = 'http://biogeo.ucdavis.edu/data/gadm2.8/gadm28_levels.gdb.zip'

    boundaries_gdb = './shapefiles/global_boundaries.gdb.zip'

    r = requests.get(boundaries_gdb_url, stream = True)

    with open(boundaries_gdb, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

def unzip_data():

    os.chdir('./shapefiles')
    boundaries_gdb_zip = ZipFile('global_boundaries.gdb.zip')
    boundaries_gdb_zip.extractall()

