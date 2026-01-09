from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from blog.models import Article, Category
from projets.models import Projet
from forum.models import Thread
from .models import NewsletterSubscription
from .forms import CommentForm

def homepage(request):
# 1. ARTICLES PUBLIÉS (Filtrer tout le site par 'is_published=True')
# Ceci garantit qu'aucun brouillon n'apparaît.
    published_articles = Article.objects.filter(is_published=True)
    
# 2. ARTICLE HERO (L'article principal)
# Prend le premier article marqué comme featured
    hero_article = published_articles.filter(is_featured=True).order_by('-publication_date').first()
    
    # 2. Récupérer toutes les catégories
    all_categories = Category.objects.all()
    main_categories = all_categories[:6]  # Les 6 premières catégories
    
# 3. DERNIERS ARTICLES
# Prend les 3 derniers articles publiés, en excluant l'article Hero (s'il existe)
# Pour s'assurer qu'il ne s'affiche pas deux fois.
    if hero_article:
         latest_articles = published_articles.exclude(pk=hero_article.pk).order_by('-publication_date')[:4]
    else:
         latest_articles = published_articles.order_by('-publication_date')[:6]
    
    # 4. DERNIERS PROJETS
    latest_projets = Projet.objects.filter(is_published=True).order_by('-publication_date')[:3]
        
    context = {
        'title': 'Accueil',
        'hero_article': hero_article,
        'latest_articles': latest_articles,
        'all_categories': all_categories,
        'main_categories': main_categories,
        'latest_projets': latest_projets,
    }
    return render(request, 'core/index.html', context)


# Newsletter Subscription View
@require_POST
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    email = request.POST.get('email', '').strip()
    
    if not email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Email requis'})
        messages.error(request, 'Veuillez fournir une adresse email.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    try:
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        
        if created:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Inscription réussie !'})
            messages.success(request, 'Merci pour votre inscription à la newsletter !')
        else:
            if not subscription.is_active:
                subscription.is_active = True
                subscription.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Réinscription réussie !'})
                messages.success(request, 'Votre abonnement a été réactivé !')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Déjà inscrit'})
                messages.info(request, 'Vous êtes déjà inscrit à la newsletter.')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Erreur lors de l\'inscription'})
        messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Search View
def search_results(request):
    """Search across articles, projects, and forum threads"""
    query = request.GET.get('q', '').strip()
    
    context = {
        'query': query,
        'articles': [],
        'projects': [],
        'threads': [],
        'total_results': 0,
        'all_categories': Category.objects.all(),
    }
    
    if query:
        # Search articles
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query),
            is_published=True
        ).distinct()[:10]
        
        # Search projects
        projects = Projet.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).distinct()[:10]
        
        # Search forum threads
        threads = Thread.objects.filter(
            Q(title__icontains=query)
        ).distinct()[:10]
        
        context['articles'] = articles
        context['projects'] = projects
        context['threads'] = threads
        context['total_results'] = articles.count() + projects.count() + threads.count()
    
    return render(request, 'core/search_results.html', context)


# Static Pages
def legal_notice(request):
    """Legal notice page"""
    context = {
        'title': 'Mentions Légales',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'core/legal.html', context)


def privacy_policy(request):
    """Privacy policy page"""
    context = {
        'title': 'Politique de Confidentialité',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'core/privacy.html', context)


def terms_of_service(request):
    """Terms of service page"""
    context = {
        'title': 'Conditions d\'Utilisation',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'core/terms.html', context)


def contact_page(request):
    """Contact page"""
    context = {
        'title': 'Contact',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'core/contact.html', context)


def sitemap_page(request):
    """HTML sitemap page"""
    context = {
        'title': 'Plan du Site',
        'all_categories': Category.objects.all(),
        'recent_articles': Article.objects.filter(is_published=True)[:10],
        'recent_projects': Projet.objects.filter(is_published=True)[:10],
    }
    return render(request, 'core/sitemap.html', context)
@require_POST
def add_comment(request, content_type_id, object_id):
    """
    Generic view to add a comment to any object (Article, Project, etc.)
    """
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour commenter.")
        # Redirect to login page with next parameter? 
        # For now, just redirect back or to login
        return redirect('login')

    try:
        content_type = ContentType.objects.get(id=content_type_id)
        # Verify that the object exists
        content_type.get_object_for_this_type(pk=object_id)
    except (ContentType.DoesNotExist, ObjectDoesNotExist):
        messages.error(request, "Le contenu que vous essayez de commenter n'existe pas.")
        return redirect('home')

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.content_type = content_type
        comment.object_id = object_id
        comment.save()
        messages.success(request, "Votre commentaire a été ajouté !")
    else:
        messages.error(request, "Erreur lors de l'ajout du commentaire. Veuillez vérifier votre saisie.")

    # Redirect back to the content object's page
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('home')
