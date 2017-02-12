from django.conf.urls import url

from . import views


app_name= 'games'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Crisis/(?P<crisis_id>[0-9]+)/$', views.crisis_detail, name='crisis_detail'),
    url(r'^Crisis\/?', views.crisis_index, name='crisis_index'),
    url(r'^Donor/(?P<donor_id>[0-9]+)/$', views.donor_detail, name='donor_detail'),
    url(r'^Donor\/?', views.donor_index, name='donor_index'),
    url(r'^Scheme/(?P<scheme_id>[0-9]+)/$', views.scheme_detail, name='scheme_detail'),
    url(r'^Scheme\/?', views.scheme_index, name='scheme_index'),
    url(r'^Person/(?P<person_id>[0-9]+)/$', views.person_detail, name='person_detail'),
    url(r'^Person\/?', views.person_index, name='person_index'),
    url(r'^Game/(?P<game_id>[0-9]+)/$', views.game_detail, name='game_detail'),
    url(r'^Game\/?', views.game_index, name='game_index')
]