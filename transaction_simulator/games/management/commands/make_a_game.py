from __future__ import unicode_literals

# Django management command imports

from django.core.management.base import BaseCommand, CommandError

# Django model imports

from games.models import *

# Constructor imports

from games.constructors.model_instances import *

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

# CONSTANTS

TRANSACTION_CATEGORY_CHOICES = [choice[0] for choice in PRODUCT_CATEGORY_CHOICES if choice[0] != "RENT"]
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
        make_game()

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

    for vendor_category in [choice[0] for choice in PRODUCT_CATEGORY_CHOICES]:

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

            earliest_time = datetime.combine(day.date(), MARKET_TIMES['open']).replace(tzinfo=pytz.utc)
            latest_time = datetime.combine(day.date(), MARKET_TIMES['close']).replace(tzinfo=pytz.utc)

            for household in scheme.clients.all():

                for spender in household.get_spenders():

                    # assume that paydays happen before any spending
                    if day.date() in altered_paydays:
                        spender.balance += decimal.Decimal(scheme.payroll_amount).quantize(decimal.Decimal('.01'))
                        spender.save()

                    # check for rent day!

                    if day.day == 1:
                        landlord = Vendor.objects.filter(category='RENT')[0]
                        transaction_time = radar.random_datetime(start=earliest_time, stop=latest_time).replace(
                            tzinfo=pytz.utc)

                        create_transaction_instance(
                            buyer=spender,
                            seller=landlord,
                            amount=RENT_AMOUNT,
                            date=transaction_time,
                            category='RENT',
                            turn=turn
                        )

                    for category in TRANSACTION_CATEGORY_CHOICES:

                        number_of_transactions = random.randint(0, 5)
                        vendor = Vendor.objects.filter(category=category)[0]

                        for transaction in range(number_of_transactions):

                            transaction_time = radar.random_datetime(start=earliest_time, stop=latest_time).replace(
                                tzinfo=pytz.utc)

                            amount = decimal.Decimal(random.uniform(10.00, 600.00)).quantize(
                                decimal.Decimal('.01'))

                            create_transaction_instance(
                                buyer=spender,
                                seller=vendor,
                                amount=amount,
                                date=transaction_time,
                                category=category,
                                turn=turn
                            )
