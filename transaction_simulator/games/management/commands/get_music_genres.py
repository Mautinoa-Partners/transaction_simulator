# Imports

#Django Management Command Imports

from django.core.management.base import BaseCommand, CommandError


# Generic Python Library Imports

import sys, os
import urllib

# Specific Python Library Imports

from bs4 import BeautifulSoup

# Requests related things

import requests
from clint.textui import progress


class Command(BaseCommand):
    args = ''
    help = 'Fetches Wikipedia Music Genre List'

    def handle(self, *args, **options):
        try:
            fetch_music_genres()

        except Exception as ex:
            raise CommandError("There was an error at the command level: %s" % (ex))
            sys.exit()

        self.success = True

        # Output mesages

        if self.success == True:
            self.stdout.write('Successfully fetched the Wikipedia list of music genres and subgenres.')

def fetch_music_genres():

    page = urllib.urlopen('https://en.wikipedia.org/wiki/List_of_popular_music_genres').read()
    soup = BeautifulSoup(page, "html.parser")

    headers = soup.find_all('span', class_='mw-headline')

    for header in headers:

        the_key = header.get_text()
        print the_key




