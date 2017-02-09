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

FILE_PATH = './games/source_data/genres.json'

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

    headers_unfiltered = soup.find_all('span', class_='mw-headline')
    unwanted_headers = ['References', 'External links', 'Bibliography', 'Exclusions']

    headers = [header for header in headers_unfiltered if header.get_text() not in unwanted_headers]

    genres_and_subgenres = {}

    dupes = []

    for header in headers:

        the_key = header.get_text().encode('utf-8')
        print "Working on header: {0}".format(the_key)

        main_genre = the_key
        subgenres = []
        u_list = header.parent.findNext('ul')

        for li in u_list.find_all('li'):

            li_text = li.get_text().encode('utf-8')

            print "Working on {0}:{1}".format(the_key,li_text)

            if li_text in dupes:

                continue

            else:

                children = [a for a in li.children]

                if len(children) == 1 and hasattr(children[0], 'text') and li.get_text() == children[0].text:

                    subgenres.append(li.get_text().encode('utf-8'))

                elif len(children) == 3 and children[1] == u' ':

                    genre_with_alias = children[0].text + ', ' + children[2].text
                    subgenres.append(genre_with_alias)

                elif len(children) > 3 and hasattr(children[0], 'text') and li.get_text().split()[0] == children[0].text:

                    new_dict = {}
                    new_key = children[0].text
                    new_sublist = li.findNext('ul')

                    new_values = [nli.get_text().encode('utf-8').strip() for nli in new_sublist.find_all('li')]

                    new_dict[new_key] = new_values
                    subgenres.append(new_dict)
                    dupes.extend(new_values)

                else:
                    print "Something really bad happened and I could not append {0}".format(li.get_text().encode('utf-8'))

        genres_and_subgenres[main_genre] = subgenres

    with open(FILE_PATH, 'wb') as outfile:
        json.dump(
            genres_and_subgenres,
            outfile,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':')
        )
