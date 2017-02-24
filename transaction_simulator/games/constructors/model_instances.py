# Django model imports

from boundaries.models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1, \
    Timezone
from games.models import *

# Python installed libraries imports

from faker import Factory
import pandas as pd

# Python Standard imports

import sys
import random
import decimal

# datetime and timezone libraries

from datetime import timedelta, datetime
import radar
import pytz
from dateutil import *
from dateutil.parser import *
from dateutil.rrule import *

# Self defined utility library

from utilities.st_functions import *
from utilities.model_object_management import *


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

# List of boundaries from large to small, with associated property names: this will be iterated over

models_and_property_names = [
    {Country: 'country'},
    {Admin_Level_1: 'admin_level_1'},
    {Admin_Level_2: 'admin_level_2'},
    {Admin_Level_3: 'admin_level_3'},
    {Admin_Level_4: 'admin_level_4'},
    {Admin_Level_5: 'admin_level_5'}
]


def create_game_instance(**kwargs):
    """"Creates a game instance, saves it and returns it"""

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.company()})

    if 'number_of_turns' not in kwargs:
        kwargs.update({'number_of_turns': random.randint(5, 20)})

    if 'crisis' not in kwargs:
        kwargs.update({'crisis': Crisis.objects.order_by('?').first() or create_crisis_instance()})

    if 'donor' not in kwargs:
        kwargs.update({'donor': Donor.objects.order_by('?').first() or create_donor_instance()})

    if 'description' not in kwargs:
        kwargs.update({'description': fake.paragraph(nb_sentences=1, variable_nb_sentences=True)})

    try:
        new_game = Game(**kwargs)
        new_game.save()
        return new_game

    except Exception as ex:
        print "There was an error creating the game. The error was {0}".format(ex)


def create_donor_instance(**kwargs):
    """Creates a donor instance, saves it and returns it"""

    if 'name' not in kwargs:
        kwargs.update({'name': random.sample(band_names, 1)[0]})

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
        kwargs.update({'name': random.sample(albums, 1)[0]})

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
        kwargs.update({'country': Country.objects.order_by('?').first()})

    if 'radius' not in kwargs:
        kwargs.update({'radius': random.uniform(0.0, 5.0)})

    if 'origin' not in kwargs:

        for random_point in generate_random_points(kwargs['country'].geom.extent):
            if kwargs['country'].geom.contains(random_point):
                break

        kwargs.update({'origin': random_point})
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

    filtered_kwargs = dict((key, value) for key, value in kwargs.iteritems() if key in ['game', 'number'])

    try:
        new_turn = Turn(**filtered_kwargs)
        new_turn.save()
        return new_turn

    except Exception as ex:
        sys.exit("There was a problem creating your Turn instance: {0}".format(ex))


def create_scheme_instance(**kwargs):
    """Creates, saves, and returns a Scheme instance"""

    if 'name' not in kwargs:
        kwargs.update({'name': random.sample(tracks, 1)[0]})

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
        kwargs.update({'crisis': Crisis.objects.order_by('?').first()})

    if 'donor' not in kwargs:
        kwargs.update({'donor': Donor.objects.order_by('?').first()})

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

    # Verify coordinates

    if 'name' not in kwargs:
        kwargs.update({'name': fake.last_name()})

    if 'coordinates' not in kwargs:
        sys.exit("You need coordinates to create a Household")

    if 'scheme' not in kwargs:
        sys.exit("You need a scheme to create a Household")

    for pairing in models_and_property_names:

        for Boundary_Model, property_field in pairing.iteritems():

            containing_boundary = which_polygon_contains_coordinates(Boundary_Model, kwargs['coordinates'])

            if containing_boundary is not None:

                kwargs.update({property_field: containing_boundary})

            else:

                continue

    try:
        new_household_instance = Household(**kwargs)
        new_household_instance.save()

    except Exception as ex:
        sys.exit("There's a problem creating your Household: {0}").format(ex)

    # Now we are going to determine the person composition of each household
    # A household is going to have some number of minors, adults, seniors
    # There must be at least one Adult but Minors and Seniors can be either zero/non-zero
    # clear kwargs

    person_kwargs = {}

    adult_count = random.choice([1, 3])
    minor_count = random.choice(range(0, 6))
    senior_count = random.choice(range(0, 5))

    # Create the adults

    for a in range(adult_count):

        # Determine sex of person because this will affect name

        sex = random.choice([choice[0] for choice in SEX_CHOICES])

        if sex == 'M':

            name = " ".join([fake.first_name_male(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_adult(**person_kwargs)

        else:

            name = " ".join([fake.first_name_female(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_adult(**person_kwargs)

    # Create the minors

    for m in range(minor_count):

        # Determine sex of person because this will affect name

        sex = random.choice([choice[0] for choice in SEX_CHOICES])

        if sex == 'M':

            name = " ".join([fake.first_name_male(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_minor(**person_kwargs)

        else:

            name = " ".join([fake.first_name_female(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_minor(**person_kwargs)

    # Create the seniors

    for s in range(senior_count):

        # Determine sex of person because this will affect name

        sex = random.choice([choice[0] for choice in SEX_CHOICES])

        if sex == 'M':

            name = " ".join([fake.first_name_male(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_minor(**person_kwargs)

        else:

            name = " ".join([fake.first_name_female(), kwargs['name']])
            person_kwargs.update({'name': name})
            person_kwargs.update({'sex': sex})
            person_kwargs.update({'household': new_household_instance})

            create_minor(**person_kwargs)


def create_minor(**kwargs):
    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme': Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age': random.randint(1, 100)})

    try:
        p = Minor(**kwargs)
        p.save()
        return p

    except Exception as ex:

        print "The error was : %s " % (ex)


def create_senior(**kwargs):
    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme': Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age': random.choice(SENIOR_AGE_RANGE)})

    try:
        p = Senior(**kwargs)
        p.save()
        return p

    except Exception as ex:

        print "The error was : %s " % (ex)


def create_adult(**kwargs):
    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme': Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age': random.choice(ADULT_AGE_RANGE)})

    try:
        p = Adult(**kwargs)
        p.save()
        return p

    except Exception as ex:

        print "The error was : %s " % (ex)


def create_person(**kwargs):
    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.person.last_name()})

    if 'scheme' not in kwargs:
        kwargs.update({'scheme': Scheme.objects.order_by('?').first()})

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    if 'age' not in kwargs:
        kwargs.update({'age': random.choice(ADULT_AGE_RANGE)})

    try:
        p = Person(**kwargs)
        p.save()
        return p

    except Exception as ex:

        print "The error was : %s " % (ex)


def create_vendor_instance(**kwargs):
    "Creates and saves a vendor instance"

    fake = Factory.create()

    # Get boundaries that intersect the crisis zone
    # and then assign the right ones based on which one contains
    # the coordinates for the vendor address

    # Verify coordinates

    if 'name' not in kwargs:
        kwargs.update({'name': fake.company()})

    if 'coordinates' not in kwargs:
        sys.exit("You need coordinates to create a Household")

    if 'balance' not in kwargs:
        kwargs.update({'balance': random.uniform(0.00, 10000.00)})

    for pairing in models_and_property_names:

        for Boundary_Model, property_field in pairing.iteritems():

            containing_boundary = which_polygon_contains_coordinates(Boundary_Model, kwargs['coordinates'])

            if containing_boundary is not None:

                kwargs.update({property_field: containing_boundary})

            else:

                continue

    try:
        new_vendor_instance = Vendor(**kwargs)
        new_vendor_instance.save()
        return new_vendor_instance

    except Exception as ex:
        print "There's a problem creating your Vendor: {0}".format(ex)
        import ipdb; ipdb.set_trace()


def create_transaction_instance(**kwargs):
    # if any(['buyer', 'seller', 'category', 'date', 'amount', 'turn']) not in kwargs:
    #     sys.exit("You are missing a required field to create a transaction.")

    # First we must record the transaction - only then will we increment accounts
    # This is an improvement over the real world, seriously.


    try:
        new_transaction_instance = Transaction(**kwargs)
        new_transaction_instance.save()

    except Exception as ex:

        import pdb;
        pdb.set_trace()
        sys.exit("There was a problem creating your Transaction: {0}".format(ex))

    # this is critical : the amount leaves the buyer's accounts before it
    # hits the seller's - this will be relevant later

    buyer = kwargs['buyer']
    seller = kwargs['seller']
    price = kwargs['amount']

    try:
        buyer.balance -= price
        buyer.save()

        seller.balance += price
        seller.save()
        return new_transaction_instance

    except Exception as ex:
        sys.exit("There was a problem with your transaction: {0}".format(ex))