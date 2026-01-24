from . import views

"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("podcast", views.podcast, name="podcast"),
    path("podcast/<int:podcast_id>/", views.podcast_detail, name="podcast_detail"),
    path("podcast-stats/", views.podcast_stats, name="podcast_stats"),
    path("recherche/", views.podcast_stats, name="podcast_recherche"), # pour recherche avancer a faire
    path("telechargement/", views.telechargement, name="download"), # por t elechargement a faire
    # pas besois de faire a propos juste ajouter un id ancre dans la page accueil.html
    path("methodologie/", views.methodologie, name="methodologie"),
    path("publication_event/", views.publication_event, name="publication_event"), # a faire
    path("contact", views.contact, name="contact")
]
