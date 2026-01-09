from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.signup, name='signup'), 
    path('edition/', views.profile_update, name='profile_update'), # NOUVEAU CHEMIN
    path('<int:pk>/', views.profil_detail, name='profil_detail'),
    path('register/', views.register_view, name='register'), # 👈 Nom utilisé dans le HTML
    # path('profils/<int:pk>/', views.profil_detail, name='profil_detail'), 
]