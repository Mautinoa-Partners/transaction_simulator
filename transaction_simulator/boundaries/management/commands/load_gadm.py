# Imports

#Django Management Command Imports

import sys

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand, CommandError
from boundaries.models import *



class Command(BaseCommand):
    args = ''
    help = 'loads the Global Adminstrative Boundaries Shapefile'

    def handle(self, *args, **options):
        try:
            # Temporarily disable Debug
            settings.configure(DEBUG=False)
            load_all_data()

        except Exception as ex:
            print "There was an error at the command level: {0}".format(ex)

        self.success = True

        # Output mesages

        if self.success == True:
            settings.configure(DEBUG=True)
            self.stdout.write('Successfully loaded the boundaries for global administrative boundaries.')


def load_all_data():

    """This is the structure function that iterates through the GADM boundaries layers and loads data."""

    # variables for data source and mappings

    ds = DataSource('shapefiles/gadm28_levels.gdb/')

    mtm = [
        {Country : country_mapping},
        {Admin_Level_5 : admin_level_5_mapping},
        {Admin_Level_4 : admin_level_4_mapping},
        {Admin_Level_3 : admin_level_3_mapping},
        {Admin_Level_2 : admin_level_2_mapping},
        {Admin_Level_1 : admin_level_1_mapping}
    ]

    # iterate through the list of model:mapping pairings and call the load function for each

    for pairing in mtm:

        layer = mtm.index(pairing)

        for mdl_df, mppng in pairing.iteritems():

            model = mdl_df
            mapping = mppng

        print "Currently working on layer %s, which is for model %s." % (layer, model)

        try:
            load_layer(ds, model, mapping, layer)

        except Exception as ex:

            raise CommandError("There was an error at the command level: %s" % (ex))

    print "All data should be loaded."

def load_layer(datasource, model, mapping, layer):

    current_count = model.objects.count()

    if current_count > 0:

        print "There are currently %s objects for %s that need to be deleted." % (current_count, model)
        model.objects.all().delete()
        print "Now they have been deleted. Current count is: %s" % (model.objects.count())

    current_count = model.objects.count()

    if current_count == 0:

        try:
            lm = LayerMapping(model, datasource, mapping, transform=True, layer=layer)
            lm.save(verbose=True, strict=False)

        except Exception as ex:

            print "There was an error at the command level: {0}".format(ex)

