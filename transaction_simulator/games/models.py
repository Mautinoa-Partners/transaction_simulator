from __future__ import unicode_literals

# GeoDjango imports

from django.contrib.gis.db import models

# Other app models

"""
Models are defined not in order of conceptual priority, but in order of necessity to
ensure that Foreign Key relations are safe.
"""

# These are some variables that will be used by all the models so I am defining them here.

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

PRODUCT_CATEGORY_CHOICES = (
    ('FOOD', 'Food'),
    ('ENTERTAINMENT', 'Entertainment'),
    ('CLOTHING', 'Clothing'),
    ('RENT', 'Rent'),
    ('UTILITIES', 'Utilities')
)

MINOR_AGE_RANGE = range(0,18)

ADULT_AGE_RANGE = range(18,56)

SENIOR_AGE_RANGE = range(56,101)

# http://stackoverflow.com/questions/6301741/django-integerfield-with-choice-options-how-to-create-0-10-integer-options
AGE_RANGE = [(i, i) for i in range(1, 100)]


# These are managers and other such utilities for the models

class MinorManager(models.Manager):

    def get_queryset(self):

        return super(MinorManager, self)\
            .get_queryset() \
            .filter(age__range=(MINOR_AGE_RANGE[0],MINOR_AGE_RANGE[-1]))

    def create(self):
        if not kwargs['age'] in MINOR_AGE_RANGE or 'age' not in kwargs:
            age = random.choice(MINOR_AGE_RANGE)
            kwargs.update({'age': age})
            return super(MinorManager, self).create(**kwargs)

        else:
            return super(MinorManager, self).create(**kwargs)


class AdultManager(models.Manager):

    def get_queryset(self):

        return super(AdultManager, self)\
            .get_queryset()\
            .filter(age__range=(ADULT_AGE_RANGE[0], ADULT_AGE_RANGE[-1]))

    def create(self):
        if not kwargs['age'] in ADULT_AGE_RANGE or 'age' not in kwargs:
            age = random.choice(ADULT_AGE_RANGE)
            kwargs.update({'age': age})
            return super(AdultManager, self).create(**kwargs)

        else:
            return super(AdultManager,self).create(**kwargs)


class SeniorManager(models.Manager):

    def get_queryset(self):

        return super(SeniorManager, self)\
            .get_queryset()\
            .filter(age__range=(SENIOR_AGE_RANGE[0], SENIOR_AGE_RANGE[-1]))

    def create(self):

        if not kwargs['age'] in SENIOR_AGE_RANGE or 'age' not in kwargs:
            age = random.choice(SENIOR_AGE_RANGE)
            kwargs.update({'age': age})
            return super(SeniorManager, self).create(**kwargs)

        else:

            return super(SeniorManager, self).create(**kwargs)

# These are the model classes

class Crisis(models.Model):
    name = models.CharField(
        max_length=200,
        default=''
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
        verbose_name="country",
        related_name="crises",
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
    def __unicode__(self):  # __unicode__ on Python 2
        return unicode(self.name)

class Donor(models.Model):
    name = models.CharField(
        default='',
        max_length=200,
    )
    home_country = models.ForeignKey(
        "boundaries.Country",
        verbose_name="country",
        related_name="donors",
        null=True,
        blank=True,
        default=1
    )

    # Returns the string representation of the model.
    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)

class Scheme(models.Model):
    name = models.CharField(
        default='',
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
        default=0.0
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
    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)

class Transaction(models.Model):
    category = models.CharField(
        max_length=1,
        choices=PRODUCT_CATEGORY_CHOICES,
        default='FOOD',
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default=0.0
    )

    buyer = models.ForeignKey(
        "games.Person",
        related_name="buyer",
        null=True
    )

    seller = models.ForeignKey(
        "games.Person",
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

    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.pk)

class Person(models.Model):
    name = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    scheme = models.ForeignKey(
        "games.Scheme",
        null=True,
        blank=True
    )

    household = models.ForeignKey(
        'games.Household',
        null=True,
        blank=True
    )

    balance = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default=0.0
    )

    transactions = models.ManyToManyField(
        'self',
        through='Transaction',
        symmetrical=False,
        related_name='transactions_for'
    )

    age = models.IntegerField(
        choices=AGE_RANGE,
        blank=True,
        null=True)

    ethnicity = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    sub_ethnicity = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    clan = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default='F',
    )

    life_points = models.IntegerField(
        default=10,
        null=True,
        blank=True
    )


    # Returns the string representation of the model.

    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)

class Minor(Person):
    objects = MinorManager()

    class Meta:
        proxy = True

class Adult(Person):
    objects = AdultManager()

    class Meta:
        proxy = True

class Senior(Person):
    objects = SeniorManager()

    class Meta:
        proxy = True

class Vendor(models.Model):
    name = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=20,
        choices=PRODUCT_CATEGORY_CHOICES,
        default='FOOD',
    )

    coordinates = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        'boundaries.Country',
        blank=True,
        null=True
    )

    admin_level_5 = models.ForeignKey(
        'boundaries.Admin_Level_5',
        blank=True,
        null=True
    )

    admin_level_4 = models.ForeignKey(
        'boundaries.Admin_Level_4',
        blank=True,
        null=True
    )

    admin_level_3 = models.ForeignKey(
        'boundaries.Admin_Level_3',
        blank=True,
        null=True
    )

    admin_level_2 = models.ForeignKey(
        'boundaries.Admin_Level_2',
        blank=True,
        null=True
    )

    admin_level_1 = models.ForeignKey(
        'boundaries.Admin_Level_1',
        blank=True,
        null=True
    )

    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)

class Household(models.Model):

    name = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    coordinates = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        'boundaries.Country',
        blank=True,
        null=True
    )

    admin_level_5 = models.ForeignKey(
        'boundaries.Admin_Level_5',
        blank=True,
        null=True
    )

    admin_level_4 = models.ForeignKey(
        'boundaries.Admin_Level_4',
        blank=True,
        null=True
    )

    admin_level_3 = models.ForeignKey(
        'boundaries.Admin_Level_3',
        blank=True,
        null=True
    )

    admin_level_2 = models.ForeignKey(
        'boundaries.Admin_Level_2',
        blank=True,
        null=True
    )

    admin_level_1 = models.ForeignKey(
        'boundaries.Admin_Level_1',
        blank=True,
        null=True
    )

    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)

class Game(models.Model):
    name = models.CharField(
        default='',
        max_length=200,
        null=True,
        blank=True
    )

    number_of_turns = models.IntegerField(
        default=10,
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
        default='',
        max_length=2000,
        null=True,
        blank=True
    )

    def __unicode__(self):  # __unicode__ on Python 2
        return u'{0}'.format(self.name)


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

    start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )



    def __unicode__(self):  # __unicode__ on Python 2

        return u'{0}'.format(pk)
