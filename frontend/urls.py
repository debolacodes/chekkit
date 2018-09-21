from django.urls import path
from django.conf.urls import include, url
from . import views

app_name= 'frontend'


from django.contrib import admin



# productsBatches
urlpatterns = [
    path('', views.overview, name='overview'),
    path('activity/', views.activity, name='activity'),
    path('analytics/', views.analytics, name='analytics'),
    path('collections/', views.collections, name='collections'),
    path('all_batches/', views.all_batches, name='all_batches'),
    path('collectionsjson/', views.collectionsJSON, name='collectionsJSON'),
    path('totalcodes/', views.totalcodes, name='totalcodes_generated'),
    path('productlines/', views.productsLines, name='productsLines'),
    path('charts/', views.charts, name='charts'),
    path('graphs/', views.graphs, name='graphs'),
    path('productcode/', views.productcode, name='productcodes'),
    path('getjson/', views.getjson, name='getjson'),
    path('productname/<int:pk>/',views.productname, name='productname')
]
