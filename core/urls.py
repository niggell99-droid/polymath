from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'), # L'URL vide ('') est la page d'accueil
]