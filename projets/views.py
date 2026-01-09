from django.shortcuts import render, get_object_or_404
from .models import Projet

def projet_list(request):
    # Recupere tous les projets publies, tries par date
    all_projets = Projet.objects.filter(is_published=True).order_by('-publication_date')

    context = {
        'projets': all_projets,
        'title': 'Tous les Projets & Tutoriels',
    }
    return render(request, 'projets/list.html', context)

def projet_detail(request, slug):
    # Recupere le projet par son slug et s'assure qu'il est publie (sinon 404)
    proje = get_object_or_404(Projet, slug=slug, is_published=True)

    context = {
        'projet': 'projet',
        # La galerie est disponible via projet.images.all dans le template
    }
    return render(request, 'projets/detail.html', context)
