from django.urls import path
from . import views


urlpatterns = [
    path('', views.toText, name='process_pdf'),
]