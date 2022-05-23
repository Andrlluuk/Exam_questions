from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:filename>', views.params, name='params')
]