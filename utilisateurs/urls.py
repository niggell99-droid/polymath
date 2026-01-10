from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='utilisateurs/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('signup/', views.signup, name='signup'),
    
    path('edition/', views.profile_update, name='profile_update'),
    path('<int:pk>/', views.profil_detail, name='profil_detail'),
    path('profils/<int:pk>/', views.profil_detail, name='profil_detail_alias'), 
]