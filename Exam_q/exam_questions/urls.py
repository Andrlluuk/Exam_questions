from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:filename>', views.params, name='params'),
    path('preview/downloadfile/<str:filename>', views.downloadfile, name='downloadfile'),
    path('preview/<str:filename>', views.preview, name='preview'),
]