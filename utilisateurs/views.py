from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def profil_detail(request, pk):
    # Cherche l'utilisateur par sa clé primaire (ID)
    user_object = get_object_or_404(User, pk=pk)

    # Le profil est accessible via la relation OneToOne
    profil = user_object.profil

    # Optionnel: Récupérer les articles et projets publiés par cet auteur (pour afficher son contenu)
    author_articles = user_object.article_set.filter(is_published=True).order_by('-publication_date')[:5]
    author_projets = user_object.projet_set.filter(is_published=True).order_by('-publication_date')[:5]

    context = {
        'user_object': user_object,
        'profil': profil,
        'author_articles': author_articles,
        'author_projets': author_projets,
        'title': f'Profil de {user_object.username}',
    }

    return render(request, 'utilisateurs/profil_detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connecte l'utilisateur immédiatement après l'inscription
            return redirect('home') # Redirige vers la page d'accueil
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': 'Inscription',
    }
    return render(request, 'registration/signup.html', context)

@login_required # Sécurise l'accès à cette vue
def profile_update(request):
    # On ne permet l'édition qu'à l'utilisateur connecté
    current_user = request.user 

    if request.method == 'POST':
        # 1. Traitement des données POST
        u_form = UserUpdateForm(request.POST, instance=current_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=current_user.profil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # Afficher un message de succès (nous ajouterons le système de messages plus tard)

            # Redirection vers la page de profil après la sauvegarde
            return redirect('profil_detail', pk=current_user.pk) 

    else:
        # 2. Initialisation des formulaires pour l'affichage (méthode GET)
        u_form = UserUpdateForm(instance=current_user)
        p_form = ProfileUpdateForm(instance=current_user.profil)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Éditer mon profil',
    }
    return render(request, 'utilisateurs/profile_update.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 1. Sauvegarde l'utilisateur (le signal de création de Profil s'exécutera ici)
            user = form.save() 
            # 2. Connecte l'utilisateur immédiatement après l'inscription (optionnel)
            login(request, user)
            # 3. Redirige vers la page d'accueil ou le profil
            return redirect('home') # Assurez-vous d'avoir un nom d'URL 'home'
    else:
        form = UserCreationForm()
        
    return render(request, 'utilisateurs/register.html', {'form': form})