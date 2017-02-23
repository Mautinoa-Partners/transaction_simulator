from __future__ import unicode_literals

# Django management command imports

from django.core.management.base import BaseCommand, CommandError

# Django model imports

from boundaries.models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1, \
    Timezone
from games.models import *

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

# Python installed libraries imports

import pandas as pd
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

# CONSTANTS

TRANSACTION_CATEGORY_CHOICES = [choice[0] for choice in PRODUCT_CATEGORY_CHOICES]
RENT_AMOUNT = decimal.Decimal(random.uniform(500.00, 1000.00)).quantize(
    decimal.Decimal('.01'))  # right now rent is in fictional currencies
MARKET_TIMES = {
    'open': datetime.strptime("7:00 AM", "%I:%M %p").time(),
    'close': datetime.strptime("10:00 PM", "%I:%M %p").time()
}


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

    if not clear_game_objects():
        sys.exit("Manually clear the game objects first.")

    # Create a shell game object with a donor, crisis and scheme

    game = Game.objects.first() or create_game_instance()

    donor = game.donor
    crisis = game.crisis
    Scheme.objects.all().delete()
    scheme = create_scheme_instance(donor=donor, crisis=crisis)

    print "Created donor, crisis, scheme, game."

    # Create turn objects for the game

    turn_count = game.number_of_turns

    if len(game.turns.all()) != turn_count:

        game.turns.all().delete()

        for t in range(1, turn_count + 1):

            try:
                create_turn_instance(game=game, number=t)
            except Exception as ex:
                sys.exit("There was a problem: {0}".format(ex))

    print "Added turns to game."

    # Determine number of households and create them
    # along with people

    household_count = random.randint(50, 100)

    for h in range(1, household_count + 1):

        # Find a point within the crisis zone for the household,
        # assign it to a variable and use that in a kwarg

        for random_point in generate_random_points(crisis.zone.extent):
            if crisis.zone.contains(random_point):
                break

        household_coordinates = random_point

        create_household_instance(coordinates=household_coordinates, scheme=scheme)

    print "Created households with adults, minors, seniors."
    # Create vendors in the zone, for now only one of each type

    for vendor_category in TRANSACTION_CATEGORY_CHOICES:

        # Find a point within the crisis zone for the vendor,
        # assign it to a variable and use that in a kwarg

        for random_point in generate_random_points(crisis.zone.extent):
            if crisis.zone.contains(random_point):
                break

        vendor_coordinates = random_point

        create_vendor_instance(coordinates=vendor_coordinates, category=vendor_category)

    print "Created one vendor of each category."

    # now comes the fun part: calculating the paydays in the scheme duration
    # The paydays matter because there the days that each person gets his balance
    # updated with a new cash infusion

    unaltered_paydays = list(rrule(
        DAILY,
        interval=14,
        dtstart=scheme.start_date,
        until=scheme.end_date))

    altered_paydays = [payday.date() for payday in unaltered_paydays]

    # now split the scheme duration up into contiguous equal blocks
    # get start date, end date for each turn and assign it

    interval_size = ((scheme.end_date - scheme.start_date) / game.number_of_turns).days

    turn_starts = list(rrule(
        DAILY,
        interval=interval_size,
        dtstart=scheme.start_date,
        until=scheme.end_date
    ))

    ordered_turns = Turn.objects.filter(game=game).order_by('number')

    for turn, turn_start in zip(ordered_turns, turn_starts):
        turn.start_date = turn_start.replace(hour=0, minute=0, second=0)
        turn.save

    # fix first turn start date: midnighting the start date could move the scheme outside the
    # duration of the crisis, so check it

    first_turn = ordered_turns.first()
    altered_start_date = first_turn.start_date

    first_turn.start_date = altered_start_date if altered_start_date <= scheme.start_date else scheme.start_date
    first_turn.save()

    end_date_interval = (((scheme.end_date - scheme.start_date) / game.number_of_turns) - timedelta(days=1)).days

    turn_ends = [turn.start_date + timedelta(days=end_date_interval) for turn in ordered_turns]

    for turn, turn_end in zip(ordered_turns, turn_ends):
        turn.end_date = turn_end.replace(hour=0, minute=0, second=0)
        turn.save()

    # fix last turn end date: midnighting the end date could move the scheme outside the duration
    # of the crisis, so check it

    last_turn = ordered_turns.last()
    altered_end_date = last_turn.end_date

    last_turn.end_date = altered_end_date if altered_end_date <= scheme.end_date else scheme.end_date

    # now comes the iteration - we are going to first iterate over turns
    # then for each day in the turn
    # then for each household in the scheme
    # get the spenders
    # check if the date is the first: if so pay rent && check if the date is a payday: if so increment balance
    # otherwise create a transaction in a random amount at a random time for each category (50/50 chance for each except rent)
    # there are no lateral transfers at this time

    for turn in ordered_turns:

        print "Now working on Turn {0}".format(turn.number)

        # create the list of days in the turn

        days_in_turn = list(rrule(
            DAILY,
            interval=1,
            dtstart=turn.start_date,
            until=turn.end_date
        ))

        for day in days_in_turn:

            print "Now working on date {0}".format(day.date())
            earliest_transaction_time = datetime.combine(day.date(), MARKET_TIMES['open'])
            latest_transaction_time = datetime.combine(day.date(), MARKET_TIMES['close'])



            for household in scheme.clients.all():

                for spender in household.get_spenders():

                    # assume that paydays happen before any spending
                    if day.date() in altered_paydays:
                        spender.balance += decimal.Decimal(scheme.payroll_amount).quantize(decimal.Decimal('.01'))
                        spender.save()

                    # check for rent day!

                    if day.day == 1:

                        landlord = Vendor.objects.filter(category='RENT')[0]
                        transaction_time = radar.random_datetime(start=earliest_time, stop=latest_time)

                        create_transaction_instance(
                            buyer=spender,
                            seller=landlord,
                            amount=RENT_AMOUNT,
                            date=transaction_time,
                            category='RENT',
                            turn=turn
                        )
                        print "{0} paid {1} in rent to {2}".format(spender.name, RENT_AMOUNT, landlord.name)


def create_game_instance(**kwargs):
    """"Creates a game instance, saves it and returns it"""

    fake = Factory.create()

    if 'name' not in kwargs:
        kwargs.update({'name': fake.company()})

    if 'number_of_turns' not in kwargs:
        kwargs.update({'number_of_turns': random.randint(1, 20)})

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
        sys.exit("There's a problem creating your Vendor: {0}").format(ex)


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
