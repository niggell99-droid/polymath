from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profil(models.Model):
    # Relation One-to-One : Un profil est lié à un seul utilisateur Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Champs personnalisés
    avatar = models.ImageField(
        default='avatars/default_user.png', # Chemin par défaut pour l'avatar (à créer dans media/)
        upload_to='avatars/'
    )
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="Votre biographie publique.")
    site_web = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)

    # Statut
    is_author = models.BooleanField(default=False, help_text="Détermine si cet utilisateur est un auteur actif du média.")

    def __str__(self):
        return f'Profil de {self.user.username}'

    def get_absolute_url(self):
        # URL du profil (nous utiliserons l'ID de l'utilisateur pour l'instant)
        return reverse('profil_detail', kwargs={'pk': self.user.pk})
