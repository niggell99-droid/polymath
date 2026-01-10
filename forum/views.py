from django.shortcuts import render, get_object_or_404
from .models import Topic, Thread, Post
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Category

# Vue 1 : Liste de tous les Thèmes (Forum Home)
def topic_list(request):
    # Récupère tous les thèmes, et utilise .annotate pour compter le nombre de sujets et messages
    # C'est une méthode d'optimisation professionnelle pour éviter les requêtes N+1.
    topics = Topic.objects.all().annotate(
        num_threads=models.Count('threads', distinct=True),
        num_posts=models.Count('threads__posts', distinct=True)
    )

    context = {
        'topics': topics,
        'title': 'Forum Communautaire',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'forum/topic_list.html', context)

# Vue 2 : Liste des Sujets pour un Thème donné
def topic_detail(request, slug):
    # Récupère le thème ou renvoie 404
    topic = get_object_or_404(Topic, slug=slug)

    # Récupère tous les sujets dans ce thème
    thread_qs = topic.threads.all().annotate(
        # Annote chaque sujet avec le nombre total de messages
        num_posts=models.Count('posts', distinct=True)
    ).order_by('-is_pinned', '-updated_at')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(thread_qs, 10)
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    context = {
        'topic': topic,
        'threads': threads,
        'title': f'Forum : {topic.name}',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'forum/topic_detail.html', context)
