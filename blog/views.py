from django.shortcuts import render, get_object_or_404
from .models import Article, Category

# Vue basée sur une fonction pour afficher un article unique
def article_detail(request, slug):
    # Tente de récupérer l'article par son slug, sinon renvoie une erreur 404
    article = get_object_or_404(Article, slug=slug, is_published=True) 

    context = {
        'article': article,
    }
    # Nous allons créer le template articles/detail.html plus tard
    return render(request, 'blog/detail.html', context)

# Liste des articles
def article_list(request):
    # Recupere tous les articles publies
    articles = Article.objects.filter(is_published=True).order_by('publication_date')

    context = {
        'articles': articles,
        'title': 'Tous les articles et Analyses',
    }
    return render(request, 'blog/list.html', context)

def category_detail(request, slug):
    # 1. Récupérer la catégorie, ou erreur 404 si elle n'existe pas
    category = get_object_or_404(Category, slug=slug)

    # 2. Récupérer tous les articles publiés dans cette catégorie
    articles = Article.objects.filter(
        category=category, 
        is_published=True
    ).order_by('-publication_date')

    context = {
        'category': category,
        'articles': articles,
        'title': f"Articles sur {category.name}",
    }
    return render(request, 'blog/category_detail.html', context)