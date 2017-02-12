from django.contrib.gis import admin
from boundaries.models import Country
from .models import Crisis, Donor, Scheme, Person, Transaction



admin.site.register(Crisis, admin.GeoModelAdmin)
admin.site.register(Donor, admin.GeoModelAdmin)
admin.site.register(Scheme, admin.GeoModelAdmin)
admin.site.register(Person, admin.GeoModelAdmin)
admin.site.register(Transaction, admin.GeoModelAdmin)

