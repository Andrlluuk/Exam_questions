from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:uuid>/load', views.load, name='load'),
    path('<str:uuid>/statistics/<str:filename>', views.statistics, name='statistics'),
    path('<str:uuid>/params/<str:filename>', views.params, name='params'),
    path('<str:uuid>/preview/downloadfile/<str:filename>', views.downloadfile, name='downloadfile'),
    path('<str:uuid>/preview/<str:filename>', views.preview, name='preview'),
    path('<str:uuid>/num_of_tickets/<str:filename>', views.params_for_tickets, name='num_of_tickets'),

]