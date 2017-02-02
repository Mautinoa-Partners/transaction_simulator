import sys, os
import urllib
import json

# Specific Python Library Imports

from bs4 import BeautifulSoup

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

                print "{0} is a duplicate. \n It was already addressed in a previous sub-list. The sublist is {1}".format(li_text,dupes)
                continue

            else:

                children = [a for a in li.children]

                if len(children) == 1 and hasattr(children[0], 'text') and li.get_text() == children[0].text:

                    subgenres.append(li.get_text().encode('utf-8'))
                    print "Just appended {0} under Condition 1".format(li.get_text().encode('utf-8'))

                elif len(children) == 3 and children[1] == u' ':

                    genre_with_alias = children[0].text + ', ' + children[2].text
                    subgenres.append(genre_with_alias)
                    print "Just appended {0} under Condition 2".format(genre_with_alias)

                elif len(children) > 3 and hasattr(children[0], 'text') and li.get_text().split()[0] == children[0].text:

                    new_dict = {}
                    new_key = children[0].text
                    new_sublist = li.findNext('ul')

                    new_values = [nli.get_text().encode('utf-8') for nli in new_sublist.find_all('li')]

                    new_dict[new_key] = new_values
                    subgenres.append(new_dict)
                    print "Just appended {0} under Condition 3".format(new_dict)
                    dupes.extend(new_values)

                else:
                    print "Something really bad happened and I could not append {0}".format(li.get_text().encode('utf-8'))

        genres_and_subgenres[main_genre] = subgenres

    print genres_and_subgenres
    import pdb; pdb.set_trace()


    with open('./games/source_data/genres.json', 'wb') as outfile:
        json.dump(
            genres_and_subgenres,
            outfile,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':')


if __name__ == '__main__':
    fetch_music_genres()






