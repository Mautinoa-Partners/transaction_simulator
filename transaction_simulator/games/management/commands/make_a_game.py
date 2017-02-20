from __future__ import unicode_literals

# Django management command imports

from django.core.management.base import BaseCommand, CommandError

# Django model imports

from boundaries.models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1
from games.models import *


# Python Standard imports

import sys
import random
from datetime import timedelta, datetime
import pytz

# Python installed libraries imports

import pandas as pd
import radar
from faker import Factory

# GEOS Geometry Types

from django.contrib.gis.geos import Point, GEOSGeometry

# Self defined utility library

from utilities.st_functions import *

# Last.fm music data for use in creating models

# Donor
band_name = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
    'artist'].dropna()
band_names = sorted(set(band_name))

# Crisis

album = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
    'album'].dropna()
albums = sorted(set(album))

# Scheme

songs = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
    'track'].dropna()
tracks = sorted(set(songs))

# Management command scaffolding

class Command(BaseCommand):
    args = ''
    help = 'makes a game'

    def handle(self, *args, **options):
        try:
            make_game()

        except Exception as ex:
            print "There was an error at the command level: {0}".format(ex)
            sys.exit()

        self.success = True

        # Output mesages

        if self.success == True:
            self.stdout.write('made a game with data')

def make_game():

    """Umbrella function for making a round"""

    print "Making a game!"

    game = Game.objects.first() or create_game_instance()

    turn_count = game.number_of_turns

    print "It has {0} turns.".format(turn_count)

    for t in range(1, turn_count+1):

        print "In {0}, Turn {1}".format(game.name, t)

    crisis_name = game.crisis.name

    print "Donor {0} is working on Crisis {1} in Country {2}".format(game.donor.name,crisis_name, game.crisis.country.name_english)

def create_game_instance(**kwargs):

    """"Creates a game instance, saves it and returns it"""

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name' : fake.company()})

    if 'number_of_turns' not in kwargs:
        kwargs.update({'number_of_turns' : random.randint(1,20)})

    if 'crisis' not in kwargs:
        kwargs.update({'crisis' : Crisis.objects.order_by('?').first() or create_crisis_instance()})


    if 'donor' not in kwargs:
        kwargs.update({'donor' : Donor.objects.order_by('?').first() or create_donor_instance()})


    if 'description' not in kwargs:
        kwargs.update({'description' : fake.paragraph(nb_sentences=1, variable_nb_sentences=True)})

    try:
        new_game = Game(**kwargs)
        new_game.save()
        return new_game

    except Exception as ex:
        print "There was an error creating the game. The error was {0}".format(ex)

def create_donor_instance(**kwargs):

    """Creates a donor instance, saves it and returns it"""

    if 'name' not in kwargs:
        kwargs.update({'name': random.sample(band_names,1)[0]})

    if 'home_country' not in kwargs:
        kwargs.update({'home_country': Country.objects.order_by('?').first()})

    try:
        new_donor = Donor(**kwargs)
        new_donor.save()
        return new_donor

    except Exception as ex:
        print "There was an error creating the donor. The error was {0}".format(ex)

def create_crisis_instance(**kwargs):

    """Creates a Crisis instance, saves it and returns it"""

    if 'name' not in kwargs:
        kwargs.update({'name': random.sample(albums,1)[0]})

    if 'start_date' not in kwargs:

        begins = radar.random_datetime(
            start=datetime(year=2000, month=5, day=24, tzinfo=pytz.utc),
            stop=datetime(year=2017, month=1, day=1, tzinfo=pytz.utc)
        )
        kwargs.update({'start_date': begins})

    if 'end_date' not in kwargs:

        ends = kwargs['start_date'] + timedelta(days=random.uniform(5, 365))
        kwargs.update({'end_date': ends})

    if 'country' not in kwargs:

        kwargs.update({'country' :Country.objects.order_by('?').first()})

    if 'radius' not in kwargs:

        kwargs.update({'radius': random.uniform(0.0,50.0)})

    if 'origin' not in kwargs:

        for random_point in generate_random_points(kwargs['country'].geom.extent):
            if kwargs['country'].geom.contains(random_point):
                break

        kwargs.update({'origin' : random_point})
        kwargs.update({'zone': random_point.buffer(kwargs['radius'])})

    if 'zone' not in kwargs:
        kwargs.update({'zone': kwargs['origin'].buffer(kwargs['radius'])})

    try:
        new_crisis = Crisis(**kwargs)
        new_crisis.save()
        return new_crisis

    except Exception as ex:

        print "There was a problem creating the crisis object. It was {0}".format(ex)
