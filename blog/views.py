from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.forms import CommentForm

# Vue basée sur une fonction pour afficher un article unique
def article_detail(request, slug):
    # Tente de récupérer l'article par son slug, sinon renvoie une erreur 404
    article = get_object_or_404(Article, slug=slug, is_published=True) 

    # Fetch comments
    comments = article.comments.filter(is_active=True).order_by('created_at')
    
    # Instantiate form
    comment_form = CommentForm()

    context = {
        'article': article,
        'all_categories': Category.objects.all(),
        'comments': comments,
        'comment_form': comment_form,
    }
    # Nous allons créer le template articles/detail.html plus tard
    return render(request, 'blog/detail.html', context)

# Liste des articles
def article_list(request):
    # Recupere tous les articles publies
    article_qs = Article.objects.filter(is_published=True).order_by('-publication_date')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(article_qs, 10)  # 10 articles par page
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'title': 'Tous les articles et Analyses',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'blog/list.html', context)

def category_detail(request, slug):
    # 1. Récupérer la catégorie, ou erreur 404 si elle n'existe pas
    category = get_object_or_404(Category, slug=slug)

    # 2. Récupérer tous les articles publiés dans cette catégorie
    article_qs = Article.objects.filter(
        category=category,
        is_published=True
    ).order_by('-publication_date')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(article_qs, 10)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'articles': articles,
        'title': f"Articles sur {category.name}",
        'all_categories': Category.objects.all(),
    }
    return render(request, 'blog/category_detail.html', context)

class CategoryArticleListView(ListView):
    model = Article
    template_name = 'blog/list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=category_slug)
        return Article.objects.filter(category=self.category, is_published=True).order_by('-publication_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Articles dans : {self.category.name}"
        context['current_category'] = self.category
        context['all_categories'] = Category.objects.all()
        return context