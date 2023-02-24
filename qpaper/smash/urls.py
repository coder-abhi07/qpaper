from django.urls import path
from . import views

handler404 = 'smash.views.handler404'

urlpatterns = [
    path('', views.upload, name='upload'),
    
]