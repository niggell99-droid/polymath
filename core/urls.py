from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Search
    path('search/', views.search_results, name='search'),
    
    # Static/Legal Pages
    path('legal/', views.legal_notice, name='legal'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('contact/', views.contact_page, name='contact'),
    path('sitemap/', views.sitemap_page, name='sitemap'),
    
    # Comments
    path('comments/add/<int:content_type_id>/<int:object_id>/', views.add_comment, name='add_comment'),
]