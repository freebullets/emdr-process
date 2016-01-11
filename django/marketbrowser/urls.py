from django.conf.urls import patterns, url

from marketbrowser import views

urlpatterns = patterns('',
    url(r'^$', views.snapshot_index, name='snapshot_index'),
    url(r'^(?P<region_id>\d+)/(?P<type_id>\d+)/$', views.snapshot_detail, name='snapshot_detail'),
    url(r'^arbitrage/$', views.arbitrage_index, name='arbitrage_index'),
    url(r'^arbitrage/(?P<from_region_id>\d+)/(?P<to_region_id>\d+)/$', views.arbitrage_detail, name='arbitrage_detail'),
    url(r'^manufacturing/$', views.manufacturing_index, name='manufacturing_index'),
    url(r'^invention/$', views.index, name='invention_index'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^autocomplete_item\.json$', views.autocomplete_item, name='autocomplete_item')
)
