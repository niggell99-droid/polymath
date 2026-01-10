from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # La page de liste des articles viendra ici plus tard
    path('', views.article_list, name='article_list'), 

    # URL de détail de l'article : /articles/mon-slug-article/
    path('categorie/<slug:slug>/', views.category_detail, name='category_detail'),

    path('categories/<slug:slug>/', views.CategoryArticleListView.as_view(), name='category_articles'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),  
]