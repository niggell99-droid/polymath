from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # 1. Page d'accueil du forum (Liste de tous les thèmes) : /forum/
    path('', views.topic_list, name='topic_list'), 

    # 2. Liste des sujets pour un thème donné : /forum/slug-du-theme/
    path('<slug:slug>/', views.topic_detail, name='topic_detail'), 

    # 3. Détail d'un sujet (Thread) : /forum/slug-du-theme/slug-du-sujet/ (sera créé plus tard)
    #path('<slug:topic_slug>/<slug:thread_slug>/', views.thread_detail, name='thread_detail'), 
]