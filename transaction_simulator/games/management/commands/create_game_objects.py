from __future__ import unicode_literals

# Django management command imports

from django.core.management.base import BaseCommand, CommandError

# Django model imports

from boundaries.models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1
from games.models import *

# GeoDjango field imports

from django.contrib.gis.geos import Point

# Python Standard imports

import inspect
import sys
import random
from datetime import timedelta, datetime
import pytz

# Python installed libraries imports

import pandas as pd
import radar
from faker import Factory


MODELS_AND_NAME_FIELDS = {

    Country : 'name_english',
    Admin_Level_5 : 'name_5',
    Admin_Level_4 : 'name_4',
    Admin_Level_3 : 'name_3',
    Admin_Level_2 : 'name_2',
    Admin_Level_1 : 'name_1',
    Crisis :'name',
    Donor : 'name',
    Scheme : 'name',
    Transaction : 'pk',
    Person : 'name',
    Vendor :'name',
    Household : 'name',
    Game : '',
    Turn : '',
    Senior : 'name'

}

# Management command scaffolding

class Command(BaseCommand):
    help = "Create objects for the games app "

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='*')

    # Variables for logic

    def handle(self, *args, **options):

        sys.setrecursionlimit(2000)

        dispatcher = {
            'donor': create_donor,
            'crisis': create_crisis,
            'scheme': create_scheme,
            'person': create_person,
            'game' : create_game,
            'turn' : create_turn
        }

        if len(options['models']) == 0:
            # do them all in order
            try:
                for creator in dispatcher:
                    dispatcher[creator]()

            except Exception as ex:
                print "There was an error in %s. \n The error was: %s" % (dispatcher[creator], ex)

        else:
            for model in options['models']:
                try:
                    dispatcher[model.lower()]()
                except KeyError as K:
                    print "Your model is not in the accepted list. You entered %s. Valid choices are: %s" % (
                    model, dispatcher.keys())

def create_donor():
    # Remove any existing objects and reset the sequences
    # There has to be a better way to do it than this.

    try:

        Donor.objects.all().delete()
        Donor.objects.raw('ALTER SEQUENCE games_donor_id_seq RESTART WITH 1;')

    except Exception as ex:
        print "Error, dipshit: %s" % ex

    print "Now working on creating Donor objects from Dheeraj's Last.Fm Band History. Donors represent agencies, so they are drawn from bands. This, of course, makes sense. \n"
    band_name = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
        'artist'].dropna()
    band_names = sorted(set(band_name))

    for bn in band_names:

        print "Now working on %s" % (bn)

        try:
            print "Now trying to create an object for: %s" % (bn)
            d = Donor(
                name=bn,
                home_country=Country.objects.order_by('?').first()
            )

            d.save()
            print "Success! Just saved Donor object %s \n with id: %s " % (d, d.id)

        except Exception as ex:

            print "Oops! There was a problem with %s. Moving on! \n" % (bn)
            print "The problem is %s" % ex
            continue

    print "Success! There are now %s Donor objects." % (Donor.objects.count())

def create_crisis():
    Crisis.objects.all().delete()

    print "Now working on creating Crisis objects from Dheeraj's Last.Fm Band History. Crises represent situations requiring remediation, so they are drawn from albums. This, of course, makes sense. \n"

    album = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
        'album'].dropna()
    albums = sorted(set(album))

    for al in albums:

        print "Now working on %s" % (al)
        crisis_name = al
        begins = radar.random_datetime(
            start=datetime(year=2000, month=5, day=24, tzinfo=pytz.utc),
            stop=datetime(year=2017, month=1, day=1, tzinfo=pytz.utc)
        )
        ends = begins + timedelta(days=random.uniform(5, 365))

        country = Country.objects.order_by('?').first()
        radius = random.uniform(0.0, 50.0)

        for random_point in generate_random_points(country.geom.extent):
            if country.geom.contains(random_point):
                break

        origin = random_point

        coverage = origin.buffer(radius)

        try:
            c = Crisis(
                name=crisis_name,
                start_date=begins,
                end_date=ends,
                country=country,
                origin=origin,
                radius=radius,
                zone=coverage
            )
            c.save()
            print "Worked! %s" % c

        except Exception as ex:

            print "The error was : %s " % (ex)
            continue

    print "Success! There are now %s Crisis objects!" % (Crisis.objects.count())

def create_scheme():
    Scheme.objects.all().delete()

    print "Now working on creating Scheme objects from Dheeraj's Last.Fm Band History. Schemes represent approaches by Donors to Crises, so they are drawn from songs. This, of course, makes sense. \n"

    songs = pd.read_csv('games/source_data/lastfm_scrobbles.csv', error_bad_lines=False, encoding='utf_8_sig')[
        'track'].dropna()
    tracks = sorted(set(songs))

    for track in tracks:

        print "Now working on %s" % (track)
        scheme_name = track
        begins = radar.random_datetime( # should be drawn from related Crisis object dates
            start=datetime(year=2000, month=5, day=24),
            stop=datetime(year=2017, month=1, day=1)
        )
        ends = begins + timedelta(days=random.uniform(5, 365))

        payroll_amount = random.uniform(100, 1000)

        crisis = Crisis.objects.order_by('?').first()
        donor = Donor.objects.order_by('?').first()

        try:
            s = Scheme(
                name=scheme_name,
                start_date=begins,
                end_date=ends,
                crisis=crisis,
                donor=donor,
                payroll_amount=payroll_amount
            )
            s.save()
            print "Worked! %s" % s

        except Exception as ex:

            print "The error was : %s " % (ex)
            continue

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
        import pdb; pdb.set_trace()

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
        import pdb; pdb.set_trace()

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
        import pdb; pdb.set_trace()

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
        p = Senior(**kwargs)

        p.save()
        print "Successfully created a person named : %s " % (kwargs['name'])

    except Exception as ex:

        print "The error was : %s " % (ex)
        import pdb; pdb.set_trace()

def create_game():
    fake = Factory.create()

    name = fake.company()

    number_of_turns = random.randint(1, 20)

    crisis = Crisis.objects.order_by('?').first()

    donor = Donor.objects.order_by('?').first()

    description = fake.paragraph(nb_sentences=1, variable_nb_sentences=True)

    try:
        g = Game(

            name=name,
            number_of_turns=number_of_turns,
            crisis=crisis,
            donor=donor,
            description=description
        )
        g.save()
        print "Successfully created a game named : %s " % (name)

    except Exception as ex:

        print "The error was : %s " % ex


def create_turn():

    print "Beginning work on assigning turns to games."
    Turn.objects.all().delete()
    games = Game.objects.all()

    for game in games:

        print "Currently building turns for game: %s, which should have %s turns." % (game.name, game.number_of_turns)
        for turn_number in range(1, game.number_of_turns+1):

            try:
                the_game = game
                the_turn_id = turn_number
                t = Turn(
                    game = the_game,
                    number = the_turn_id
                 )

                t.save()
                print "Successfully created a Turn: %s for Game: %s" % (the_turn_id, the_game)

            except Exception as ex:
                print "There was a problem creating a Turn: %s for Game: %s" % (the_turn_id, the_game)

### HELPER FUNCTIONS ###

def read_music_data_for_ethnicity():
    print "Music!"


def get_object_by_name_or_id(test_model, name, search_type='iexact'):

    # ensure we have a good model

    if test_model not in MODELS_AND_NAME_FIELDS.keys():

        sys.exit('You have specified an invalid model. Please choose from: {0}'.format(MODELS_AND_NAME_FIELDS.keys()))

    else:

        test_field = MODELS_AND_NAME_FIELDS[test_model]
        filtration = test_field + '__' + search_type

        try:
            the_objects = test_model.objects.filter(**{filtration : name})

            if len(the_objects) > 1:
                return the_objects[0]
            else:
                return the_objects

        except Exception:

            print ('Searching by PK instead')

            if int(name):
                name = int(name)
                try:
                    the_object = test_model.objects.get(pk=name)
                    return the_object

                except Exception as ex:

                    print "{0} was the exception".format(ex)


# def generate_household(**kwargs):




def generate_random_points(bounding_box):
    yield Point(
        x=random.uniform(bounding_box[0], bounding_box[2]),
        y=random.uniform(bounding_box[1], bounding_box[2])
    )

def get_random_object(model):
    primo = model.objects.first()
    ultimo = model.objects.last()
    try:
        the_object = model.objects.get(pk=random.randint(primo.id, ultimo.id))
        return the_object
    except Exception as ex:
        get_random_object(model)
