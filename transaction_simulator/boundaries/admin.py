from django.contrib.gis import admin
from .models import Country, Admin_Level_5, Admin_Level_4, Admin_Level_3, Admin_Level_2, Admin_Level_1

admin.site.register(Country, admin.OSMGeoAdmin)
# admin.site.register(Admin_Level_5, admin.OSMGeoAdmin)
# admin.site.register(Admin_Level_4, admin.OSMGeoAdmin)
# admin.site.register(Admin_Level_3, admin.OSMGeoAdmin)
# admin.site.register(Admin_Level_2, admin.OSMGeoAdmin)
# admin.site.register(Admin_Level_1, admin.OSMGeoAdmin)