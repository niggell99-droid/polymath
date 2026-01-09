"""
URL configuration for config project.

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
from django.urls import path, include
# Imports pour les fichiers media en mode développement
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('projets/', include('projets.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('profils/', include('utilisateurs.urls')),
    path('comptes/', include('django.contrib.auth.urls')),
    path('forum/', include('forum.urls')),
]

# NE JAMAIS UTILISER CECI EN PRODUCTION ! UNIQUEMENT POUR LE DÉVELOPPEMENT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
