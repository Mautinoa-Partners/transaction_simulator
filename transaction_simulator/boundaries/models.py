from __future__ import unicode_literals
from django.contrib.gis.db import models

# Create your models here.

class Country(models.Model):

    # Regular Django fields

    id_0 = models.IntegerField()
    iso = models.CharField(max_length=300)
    name_english = models.CharField(max_length=300)
    waspartof = models.CharField(max_length=300)
    contains = models.CharField(max_length=300)
    sovereign = models.CharField(max_length=300)
    iso2 = models.CharField(max_length=300)
    www = models.CharField(max_length=300)
    fips = models.CharField(max_length=300)
    ison = models.FloatField()
    validfr = models.CharField(max_length=300)
    validto = models.CharField(max_length=300)
    pop2000 = models.FloatField()
    sqkm = models.FloatField()
    popsqkm = models.FloatField()
    unregion1 = models.CharField(max_length=300)
    unregion2 = models.CharField(max_length=300)
    developing = models.FloatField()
    cis = models.FloatField()
    transition = models.FloatField()
    oecd = models.FloatField()
    wbregion = models.CharField(max_length=300)
    wbincome = models.CharField(max_length=300)
    wbdebt = models.CharField(max_length=300)
    wbother = models.CharField(max_length=300)
    ceeac = models.FloatField()
    cemac = models.FloatField()
    ceplg = models.FloatField()
    comesa = models.FloatField()
    eac = models.FloatField()
    ecowas = models.FloatField()
    igad = models.FloatField()
    ioc = models.FloatField()
    mru = models.FloatField()
    sacu = models.FloatField()
    uemoa = models.FloatField()
    uma = models.FloatField()
    palop = models.FloatField()
    parta = models.FloatField()
    cacm = models.FloatField()
    eurasec = models.FloatField()
    agadir = models.FloatField()
    saarc = models.FloatField()
    asean = models.FloatField()
    nafta = models.FloatField()
    gcc = models.FloatField()
    csn = models.FloatField()
    caricom = models.FloatField()
    eu = models.FloatField()
    can = models.FloatField()
    acp = models.FloatField()
    landlocked = models.FloatField()
    aosis = models.FloatField()
    sids = models.FloatField()
    islands = models.FloatField()
    ldc = models.FloatField()
    shape_length = models.FloatField()
    shape_area = models.FloatField()

    # GeoDjango Geometry

    geom = models.MultiPolygonField(srid=4326)

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name_english

class Admin_Level_5(models.Model):
    id_0 = models.IntegerField(blank=True)
    iso = models.CharField(max_length=300, blank=True)
    name_0 = models.CharField(max_length=300, blank=True)
    id_1 = models.IntegerField(blank=True)
    name_1 = models.CharField(max_length=300, blank=True)
    id_2 = models.IntegerField(blank=True)
    name_2 = models.CharField(max_length=300, blank=True)
    id_3 = models.IntegerField(blank=True)
    name_3 = models.CharField(max_length=300, blank=True)
    id_4 = models.IntegerField(blank=True)
    name_4 = models.CharField(max_length=300, blank=True)
    id_5 = models.IntegerField(blank=True)
    name_5 = models.CharField(max_length=300, blank=True)
    ccn_5 = models.IntegerField(blank=True)
    cca_5 = models.CharField(max_length=300, blank=True)
    type_5 = models.CharField(max_length=300, blank=True)
    engtype_5 = models.CharField(max_length=300, blank=True)
    shape_length = models.FloatField(blank=True)
    shape_area = models.FloatField(blank=True)

    # GeoDjango Geometry

    geom = models.MultiPolygonField(srid=4326)

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name_5

class Admin_Level_4(models.Model):
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=300)
    name_0 = models.CharField(max_length=300)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=300)
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=300)
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=300)
    id_4 = models.IntegerField()
    name_4 = models.CharField(max_length=300)
    varname_4 = models.CharField(max_length=300)
    ccn_4 = models.IntegerField()
    cca_4 = models.CharField(max_length=300)
    type_4 = models.CharField(max_length=300)
    engtype_4 = models.CharField(max_length=300)
    shape_length = models.FloatField()
    shape_area = models.FloatField()

    # GeoDjango Geometry

    geom = models.MultiPolygonField(srid=4326)

    # Returns the string representation of the model.

    def __unicode__(self): return self.name_4

class Admin_Level_3(models.Model):
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=300)
    name_0 = models.CharField(max_length=300)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=300)
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=300)
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=300)
    ccn_3 = models.IntegerField()
    cca_3 = models.CharField(max_length=300)
    type_3 = models.CharField(max_length=300)
    engtype_3 = models.CharField(max_length=300)
    nl_name_3 = models.CharField(max_length=300)
    varname_3 = models.CharField(max_length=300)
    shape_length = models.FloatField()
    shape_area = models.FloatField()

    # GeoDjango Geometry

    geom = models.MultiPolygonField(srid=4326)

    # Returns the string representation of the model.

    def __unicode__(self): return self.name_3

class Admin_Level_2(models.Model):
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=300)
    name_0 = models.CharField(max_length=300)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=300)
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=300)
    hasc_2 = models.CharField(max_length=300)
    ccn_2 = models.IntegerField()
    cca_2 = models.CharField(max_length=300)
    type_2 = models.CharField(max_length=300)
    engtype_2 = models.CharField(max_length=300)
    nl_name_2 = models.CharField(max_length=300)
    varname_2 = models.CharField(max_length=300)
    shape_length = models.FloatField()
    shape_area = models.FloatField()

    # GeoDjango Geometry

    geom = models.MultiPolygonField(srid=4326)

    # Returns the string representation of the model.
    def __unicode__(self): return self.name_2

class Admin_Level_1(models.Model):
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=300)
    name_0 = models.CharField(max_length=300)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=300)
    hasc_1 = models.CharField(max_length=300)
    ccn_1 = models.IntegerField()
    cca_1 = models.CharField(max_length=300)
    type_1 = models.CharField(max_length=300)
    engtype_1 = models.CharField(max_length=300)
    nl_name_1 = models.CharField(max_length=300)
    varname_1 = models.CharField(max_length=300)
    shape_length = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __unicode__(self): return self.name_1

class Timezone(models.Model):
    tzid = models.CharField(max_length=30)
    geom = models.MultiPolygonField()

    def __unicode__(self):

        return unicode(self.tzid)

country_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_english' : 'NAME_ENGLISH',
    'waspartof' : 'WASPARTOF',
    'contains' : 'CONTAINS',
    'sovereign' : 'SOVEREIGN',
    'iso2' : 'ISO2',
    'www' : 'WWW',
    'fips' : 'FIPS',
    'ison' : 'ISON',
    'validfr' : 'VALIDFR',
    'validto' : 'VALIDTO',
    'pop2000' : 'POP2000',
    'sqkm' : 'SQKM',
    'popsqkm' : 'POPSQKM',
    'unregion1' : 'UNREGION1',
    'unregion2' : 'UNREGION2',
    'developing' : 'DEVELOPING',
    'cis' : 'CIS',
    'transition' : 'Transition',
    'oecd' : 'OECD',
    'wbregion' : 'WBREGION',
    'wbincome' : 'WBINCOME',
    'wbdebt' : 'WBDEBT',
    'wbother' : 'WBOTHER',
    'ceeac' : 'CEEAC',
    'cemac' : 'CEMAC',
    'ceplg' : 'CEPLG',
    'comesa' : 'COMESA',
    'eac' : 'EAC',
    'ecowas' : 'ECOWAS',
    'igad' : 'IGAD',
    'ioc' : 'IOC',
    'mru' : 'MRU',
    'sacu' : 'SACU',
    'uemoa' : 'UEMOA',
    'uma' : 'UMA',
    'palop' : 'PALOP',
    'parta' : 'PARTA',
    'cacm' : 'CACM',
    'eurasec' : 'EurAsEC',
    'agadir' : 'Agadir',
    'saarc' : 'SAARC',
    'asean' : 'ASEAN',
    'nafta' : 'NAFTA',
    'gcc' : 'GCC',
    'csn' : 'CSN',
    'caricom' : 'CARICOM',
    'eu' : 'EU',
    'can' : 'CAN',
    'acp' : 'ACP',
    'landlocked' : 'Landlocked',
    'aosis' : 'AOSIS',
    'sids' : 'SIDS',
    'islands' : 'Islands',
    'ldc' : 'LDC',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

admin_level_5_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_0' : 'NAME_0',
    'id_1' : 'ID_1',
    'name_1' : 'NAME_1',
    'id_2' : 'ID_2',
    'name_2' : 'NAME_2',
    'id_3' : 'ID_3',
    'name_3' : 'NAME_3',
    'id_4' : 'ID_4',
    'name_4' : 'NAME_4',
    'id_5' : 'ID_5',
    'name_5' : 'NAME_5',
    'ccn_5' : 'CCN_5',
    'cca_5' : 'CCA_5',
    'type_5' : 'TYPE_5',
    'engtype_5' : 'ENGTYPE_5',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

admin_level_4_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_0' : 'NAME_0',
    'id_1' : 'ID_1',
    'name_1' : 'NAME_1',
    'id_2' : 'ID_2',
    'name_2' : 'NAME_2',
    'id_3' : 'ID_3',
    'name_3' : 'NAME_3',
    'id_4' : 'ID_4',
    'name_4' : 'NAME_4',
    'varname_4' : 'VARNAME_4',
    'ccn_4' : 'CCN_4',
    'cca_4' : 'CCA_4',
    'type_4' : 'TYPE_4',
    'engtype_4' : 'ENGTYPE_4',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

admin_level_3_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_0' : 'NAME_0',
    'id_1' : 'ID_1',
    'name_1' : 'NAME_1',
    'id_2' : 'ID_2',
    'name_2' : 'NAME_2',
    'id_3' : 'ID_3',
    'name_3' : 'NAME_3',
    'ccn_3' : 'CCN_3',
    'cca_3' : 'CCA_3',
    'type_3' : 'TYPE_3',
    'engtype_3' : 'ENGTYPE_3',
    'nl_name_3' : 'NL_NAME_3',
    'varname_3' : 'VARNAME_3',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

admin_level_2_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_0' : 'NAME_0',
    'id_1' : 'ID_1',
    'name_1' : 'NAME_1',
    'id_2' : 'ID_2',
    'name_2' : 'NAME_2',
    'hasc_2' : 'HASC_2',
    'ccn_2' : 'CCN_2',
    'cca_2' : 'CCA_2',
    'type_2' : 'TYPE_2',
    'engtype_2' : 'ENGTYPE_2',
    'nl_name_2' : 'NL_NAME_2',
    'varname_2' : 'VARNAME_2',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

admin_level_1_mapping = {
    'id_0' : 'ID_0',
    'iso' : 'ISO',
    'name_0' : 'NAME_0',
    'id_1' : 'ID_1',
    'name_1' : 'NAME_1',
    'hasc_1' : 'HASC_1',
    'ccn_1' : 'CCN_1',
    'cca_1' : 'CCA_1',
    'type_1' : 'TYPE_1',
    'engtype_1' : 'ENGTYPE_1',
    'nl_name_1' : 'NL_NAME_1',
    'varname_1' : 'VARNAME_1',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

timezone_mapping = {
    'tzid' : 'TZID',
    'geom' : 'MULTIPOLYGON',
}