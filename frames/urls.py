from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


# url(r'^(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$', views.index, name='index'),
urlpatterns = [

    url(r'^analytics/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',TemplateView.as_view(template_name="analytics/codes_over_products.html"), name='frame_analytics'),
    url(r'^locations/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',TemplateView.as_view(template_name="analytics/codes_over_locations.html"), name='frame_locations'),
    url(r'^complaints/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',TemplateView.as_view(template_name="analytics/codes_over_complaints.html"), name='frame_complaints'),
    
];
