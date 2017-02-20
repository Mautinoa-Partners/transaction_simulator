from __future__ import unicode_literals

# Django management command imports

from django.core.management.base import BaseCommand, CommandError

# Django model imports

from boundaries.models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1, Timezone
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

# List of boundaries from large to small, with associated property names: this will be iterated over

models_and_property_names = [
    {Country: 'country'},
    {Admin_Level_1: 'admin_level_1'},
    {Admin_Level_2: 'admin_level_2'},
    {Admin_Level_3: 'admin_level_3'},
    {Admin_Level_4: 'admin_level_4'},
    {Admin_Level_5: 'admin_level_5'}
]

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

    # Create a shell game object with a donor, crisis and scheme

    game = Game.objects.first() or create_game_instance()

    scheme = create_scheme_instance(donor=game.donor, crisis=game.crisis)
    donor = game.donor
    crisis = game.crisis

    print "Successfully created a scheme: {0}".format(scheme.name)

    # Create turn objects for the game
    turn_count = game.number_of_turns

    print "It has {0} turns.".format(turn_count)

    for t in range(1, turn_count+1):

        print "In {0}, Turn {1}".format(game.name, t)
        try:
            create_turn_instance(game=game, number=t)
            print "Successfully created Turn: {0} for Game {1}".format(t,game)
        except Exception as ex:
            sys.exit("There was a problem: {0}".format(ex))

    # Determine number of households and create them

    household_count = random.randint(50,100)

    for h in range(1, household_count+1):

        # Find a point within the crisis zone for the household,
        # assign it to a variable and use that in a kwarg

        for random_point in generate_random_points(crisis.zone.extent):
            if crisis.zone.contains(random_point):
                break

        household_coordinates = random_point

        create_household_instance(coordinates=household_coordinates)
        print "Successfully created a household!"

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

        kwargs.update({'radius': random.uniform(0.0,5.0)})

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

def create_turn_instance(**kwargs):

    """Creates, saves and returns a Turn instance"""

    if 'number' not in kwargs:
        sys.exit("You need to specify the turn number")

    if 'game' not in kwargs:
        sys.exit("You need to specify the game")

    filtered_kwargs = dict((key,value) for key, value in kwargs.iteritems() if key in ['game', 'number'])

    try:
        new_turn = Turn(**filtered_kwargs)
        new_turn.save()
        return new_turn

    except Exception as ex:
        sys.exit("There was a problem creating your Turn instance: {0}".format(ex))

def create_scheme_instance(**kwargs):

    """Creates, saves, and returns a Scheme instance"""

    if 'name' not in kwargs:
        kwargs.update({'name': random.sample(tracks,1)[0]})

    if 'start_date' not in kwargs:

        begins = radar.random_datetime(
            start=datetime(year=2000, month=5, day=24, tzinfo=pytz.utc),
            stop=datetime(year=2017, month=1, day=1, tzinfo=pytz.utc)
        )
        kwargs.update({'start_date': begins})

    if 'end_date' not in kwargs:

        ends = kwargs['start_date'] + timedelta(days=random.uniform(5, 365))
        kwargs.update({'end_date': ends})

    if 'payroll_amount' not in kwargs:
        kwargs.update({'payroll_amount': random.uniform(100, 1000)})

    if 'crisis' not in kwargs:
        kwargs.update({'crisis': Crisis.objects.order_by('?').first() })

    if 'donor' not in kwargs:
        kwargs.update({'donor': Donor.objects.order_by('?').first() })


    try:
        new_scheme = Scheme(**kwargs)
        new_scheme.save()
        return new_scheme

    except Exception as ex:
        print "There was a problem creating your Scheme: {0}".format(ex)

def create_household_instance(**kwargs):

    "Creates and saves a household instance"

    fake = Factory.create()

    # Get boundaries that intersect the crisis zone
    # and then assign the right ones based on which one contains
    # the coordinates for the household address

    # Verify coordinates and zone

    if 'name' not in kwargs:
        kwargs.update({'name': fake.last_name()})

    if 'coordinates' not in kwargs:
        sys.exit("You need coordinates to create a Household")

    for pairing in models_and_property_names:

        for Boundary_Model, property_field in pairing.iteritems():

            containing_boundary = which_polygon_contains_coordinates(Boundary_Model, kwargs['coordinates'])

            if containing_boundary is not None:

                kwargs.update({property_field:containing_boundary})

            else:

                continue

    try:
        new_household_instance = Household(**kwargs)
        new_household_instance.save()
        print "Saved a household: {0}".format(new_household_instance)

    except Exception as ex:
        sys.exit("There's a problem creating your Household: {0}").format(ex)

    # Now we are going to determine the person composition of each household
    # A household is going to have some number of minors, adults, seniors
    # There must be at least one Adult but Minors and Seniors can be either zero/non-zero
    # clear kwargs

    person_kwargs = {}

    adult_count = random.choice([1,3])
    minor_count = random.choice(range(0,6))
    senior_count = random.choice(range(0, 5))

    # Create the adults

    print "Gotta make {0} adults".format(adult_count)
    for a in range(adult_count):

        # Determine sex of person because this will affect name

        sex = random.choice([choice[0] for choice in SEX_CHOICES])

        if sex == 'M':

            print "It's a boy!"

            name = " ".join([fake.first_name_male(), kwargs['name']])
            person_kwargs.update({'name' : name})
            person_kwargs.update({'sex' : sex})
            person_kwargs.update({'household' : new_household_instance})

            create_adult(**person_kwargs)

        else:

            print "It's a girl!"

            name = " ".join([fake.first_name_female(), kwargs['name']])
            person_kwargs.update({'name' : name})
            person_kwargs.update({'sex' : sex})
            person_kwargs.update({'household' : new_household_instance})


            create_adult(**person_kwargs)

    # Create the minors

    print "Gotta make {0} minors".format(minor_count)

    for m in range(minor_count):

        # Determine sex of person because this will affect name

        sex = random.choice([choice[0] for choice in SEX_CHOICES])

        if sex == 'M':

            print "It's a boy!"

            name = " ".join([fake.first_name_male(), kwargs['name']])
            person_kwargs.update({'name' : name})
            person_kwargs.update({'sex' : sex})
            person_kwargs.update({'household' : new_household_instance})


            create_minor(**person_kwargs)

        else:

            print "It's a girl!"

            name = " ".join([fake.first_name_female(), kwargs['name']])
            person_kwargs.update({'name' : name})
            person_kwargs.update({'sex' : sex})
            person_kwargs.update({'household' : new_household_instance})


            create_minor(**person_kwargs)





def create_minor(**kwargs):

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme':  Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age' : random.randint(1,100)})

    try:
        p = Minor(**kwargs)

        p.save()
        print "Successfully created a person named : %s " % (kwargs['name'])

    except Exception as ex:

        print "The error was : %s " % (ex)

def create_senior(**kwargs):

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme':  Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age' : random.choice(SENIOR_AGE_RANGE)})

    try:
        p = Senior(**kwargs)

        p.save()
        print "Successfully created a person named : %s " % (kwargs['name'])

    except Exception as ex:

        print "The error was : %s " % (ex)

def create_adult(**kwargs):

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme':  Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age' : random.choice(ADULT_AGE_RANGE)})

    try:
        p = Adult(**kwargs)

        p.save()
        print "Successfully created a person named : %s " % (kwargs['name'])

    except Exception as ex:

        print "The error was : %s " % (ex)

def create_person(**kwargs):

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.person.last_name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme':  Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age' : random.choice(ADULT_AGE_RANGE)})

    try:
        p = Person(**kwargs)

        p.save()
        print "Successfully created a person named : %s " % (kwargs['name'])

    except Exception as ex:

        print "The error was : %s " % (ex)