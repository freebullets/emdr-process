from django.conf.urls import patterns, url

from marketbrowser import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<region_id>\d+)/(?P<type_id>\d+)/$', views.detail, name='detail'),
    url(r'^arbitrage/$', views.arbitrage_index, name='arbitrage_index'),
    url(r'^arbitrage/(?P<from_region_id>\d+)/(?P<to_region_id>\d+)/$', views.arbitrage, name='arbitrage'),
    url(r'^autocomplete_item\.json$', views.autocomplete_item, name='autocomplete_item')
)