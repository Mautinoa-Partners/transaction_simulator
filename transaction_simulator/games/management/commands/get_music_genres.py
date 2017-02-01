# https://kazuar.github.io/scrape-wikipedia-tutorial/

# Imports

#Django Management Command Imports

from django.core.management.base import BaseCommand, CommandError


# Generic Python Library Imports

import sys, os
import urllib
import json

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
    unwanted_headers = ['References', 'External links', 'Bibliography', 'Exclusions']

    genres_and_subgenres = {}

    for header in headers:

        the_key = header.get_text()

        if the_key in unwanted_headers:

            continue

        else:

            main_genre = the_key
            u_list = header.parent.findNext('ul')
            subgenres = [li.get_text().replace("\n"," ").replace("  "," ").encode('utf-8') for li in u_list.find_all('li')]

            genres_and_subgenres[main_genre] = subgenres

    print genres_and_subgenres

    with open('./games/source_data/genres.json', 'wb') as outfile:
        json.dump(
            genres_and_subgenres,
            outfile,
            indent=4,
            ensure_ascii=False,
            encoding='utf-8',
            sort_keys=True,
            separators=(',', ':')
                  )









