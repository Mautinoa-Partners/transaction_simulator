from __future__ import unicode_literals

#GeoDjango imports

from django.contrib.gis.db import models

# Other app models

"""
Models are defined not in order of conceptual priority, but in order of necessity to
ensure that Foreign Key relations are safe.
"""

# These are some variables that will be used by all the models so I am defining them here.


class Crisis(models.Model):

    name = models.CharField(
        max_length=200,
        default =''
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )
    radius = models.DecimalField(
        max_digits=14,
        decimal_places=6
    )
    country = models.ForeignKey(
        "boundaries.Country",
        verbose_name= "country",
        related_name = "crises",
        null=True,
        blank=True,
        default=1
    )

    origin = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )

    zone = models.PolygonField(
        srid=4326,
        null=True,
        blank=True
    )

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Donor(models.Model):

    name = models.CharField(
        default = '',
        max_length=200,
    )
    home_country = models.ForeignKey(
        "boundaries.Country",
        verbose_name= "country",
        related_name = "donors",
        null=True,
        blank=True,
        default=1
    )

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Scheme(models.Model):

    name = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    payroll_amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default = 0.0
    )

    donor = models.ForeignKey(
        'games.Donor',
        related_name='schemes',
        blank=True,
        null=True
    )

    crisis = models.ForeignKey(
        'games.Crisis',
        related_name='scheme',
        null=True
    )

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Person(models.Model):

    name = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    scheme = models.ForeignKey(
        Scheme,
        null=True,
        blank=True
    )

    balance = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default = 0.0
     )

    transactions = models.ManyToManyField(
        'self',
        through='Transaction',
        symmetrical=False,
        related_name='transactions_for'
    )

    age = models.IntegerField(
        choices=[(i, i) for i in range(1, 100)],
        blank=True,
        null=True)

    ethnicity = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    sub_ethnicity = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    clan = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    # Returns the string representation of the model.

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Transaction(models.Model):

    CATEGORY_CHOICES= (
        ('FOOD', 'Food'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('CLOTHING', 'Clothing'),
        ('RENT', 'Rent'),
        ('UTILITIES', 'Utilities')
    )

    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='FOOD',
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default = 0.0
     )

    buyer = models.ForeignKey(
        Person,
        related_name = "buyer",
        null=True
    )

    seller = models.ForeignKey(
        Person,
        related_name="seller",
        null=True
    )

    date = models.DateTimeField(
        null=True,
        blank=True
    )

    turn = models.ForeignKey(
        'games.Turn',
        related_name='transactions',
        blank=True,
        null=True
    )

    def __unicode__(self):              # __unicode__ on Python 2
        return self.pk

class Game(models.Model):

    name = models.CharField(
        default = '',
        max_length=200,
        null=True,
        blank=True
    )

    number_of_turns = models.IntegerField(
        default = 10,
        null=True,
        blank=True
    )

    crisis = models.ForeignKey(
        'games.Crisis',
        related_name='games',
        null=True
    )

    donor = models.ForeignKey(
        'games.Donor',
        related_name='games',
        blank=True,
        null=True
    )

    description = models.CharField(
        default = '',
        max_length = 2000,
        null=True,
        blank=True
    )

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Turn(models.Model):

    game = models.ForeignKey(
        'games.Game',
        related_name='turns',
        null=True,
        blank=True
    )

    number = models.IntegerField(
        default=1,
        null=True,
        blank=True
    )

    def __unicode__(self):              # __unicode__ on Python 2

        identifying_string = 'Game: %s, Turn %s' % (str(self.game), str(self.number))
        return identifying_string





