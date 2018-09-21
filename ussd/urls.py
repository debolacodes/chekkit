from django.conf.urls import url
from . import views


# url(r'^(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$', views.index, name='index'),
urlpatterns = [
    url(r'^$',views.ussddata, name='ussddata'),
    url(r'^totalcodes/$',views.totalcodes, name='totalcodes_tracked'),

    url(r'^pl/(?P<pl>\d+)/$',views.ussddatapl, name='ussddatapl'),
    url(r'^pl/(?P<pl>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$', views.ussddatarangepl, name='ussddatarangeplpl'),
    url(r'^pl/(?P<pl>\d+)/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$',views.ussddatadaypl, name='ussddatadaypl'),
    url(r'^pl/(?P<pl>\d+)/(?P<date>[0-9]{4})/$',views.ussddatayearpl, name='ussddatayearpl'),
    url(r'^pl/(?P<pl>\d+)/(?P<date>[0-9]{4}-?[0-9]{2})/$',views.ussddatamonthpl, name='ussddatamonthpl'),


    url(r'^(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$', views.ussddatarange, name='ussddatarange'),
    url(r'^(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$',views.ussddataday, name='ussddataday'),
    url(r'^(?P<date>[0-9]{4})/$',views.ussddatayear, name='ussddatayear'),
    url(r'^(?P<date>[0-9]{4}-?[0-9]{2})/$',views.ussddatamonth, name='ussddatamonth'),
    # get ussd data for specific products
    url(r'^analytics/$',views.analytics, name='analytics'),
    url(r'^locations/$',views.analytics_locations, name='analytics'),
    url(r'^cc/$',views.analytics_codechecked, name='analytics'),
    # url(r'^cc/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.codes_checked_range, name='analytics'),
    url(r'^complaints/$',views.analytics_complaints, name='complaints'),
    # get ussd data products
    url(r'^analytics/(?P<product_id>\d+)/$',views.analytics_product, name='analytics'),
    url(r'^locations/(?P<product_id>\d+)/$',views.analytics_locations_product, name='analytics'),
    url(r'^cc/(?P<product_id>\d+)/$',views.analytics_codechecked_product, name='analytics'),
    url(r'^complaints/(?P<product_id>\d+)/$',views.analytics_complaints_product, name='complaints'),
    # get ussd data for specific products with daterange
    url(r'^analytics/(?P<product_id>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.analytics_product_range, name='analytics'),
    url(r'^locations/(?P<product_id>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.analytics_locations_product_range, name='analytics'),
    url(r'^cc/(?P<product_id>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.analytics_codechecked_product_range, name='analytics'),
    url(r'^complaints/(?P<product_id>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.analytics_complaints_product_range, name='complaints'),
    url(r'^checked/(?P<product_id>\d+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',views.analytics_codechecked_perday_product_range, name='complaints'),
];
