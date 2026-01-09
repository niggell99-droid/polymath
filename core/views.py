from django.shortcuts import render
# Importez le modèle Article pour interroger la base de données
from blog.models import Article

def homepage(request):
# 1. ARTICLES PUBLIÉS (Filtrer tout le site par 'is_published=True')
# Ceci garantit qu'aucun brouillon n'apparaît.
    published_articles = Article.objects.filter(is_published=True)
    
# 2. ARTICLE HERO (L'article principal)
# Cherche le premier article marqué comme "featured" (is_featured=True) et le trie par date de publication.
    hero_article = published_articles.filter(is_featured=True).order_by('-publication_date').first()
    
# 3. DERNIERS ARTICLES
# Prend les 3 derniers articles publiés, en excluant l'article Hero (s'il existe)
# Pour s'assurer qu'il ne s'affiche pas deux fois.
    if hero_article:
         latest_articles = published_articles.exclude(pk=hero_article.pk).order_by('-publication_date')[:3]
    else:
         latest_articles = published_articles.order_by('-publication_date')[:6]
        
    context = {
        'title': 'Accueil',
        'hero_article': hero_article,
        'latest_articles': latest_articles,
    }
    return render(request, 'core/index.html', context)


"""# core/views.py
from django.shortcuts import render
# Importez vos modèles des applications
from blog.models import Article, Category # AJOUT DE Category
# from projets.models import Projet

def homepage(request):
    # 1. Derniers Articles (comme avant)
    latest_articles = Article.objects.filter(is_published=True).order_by('-publication_date')[:6]

    # 2. Article 'Hero' (le plus récent ou un spécial)
    hero_article = latest_articles.first()

    # 3. Catégories Principales (Exemple : les 4 premières catégories triées par nom)
    main_categories = Category.objects.all().order_by('name')[:4] 

    # 4. Derniers Projets (pour la section Projets si vous l'ajoutez)
    # latest_projets = Projet.objects.filter(is_published=True).order_by('-publication_date')[:3]

    context = {
        'latest_articles': latest_articles,
        'hero_article': hero_article,
        'main_categories': main_categories, # NOUVELLE VARIABLE
        # 'latest_projets': latest_projets, # NOUVELLE VARIABLE
    }
    return render(request, 'core/homepage.html', context)"""