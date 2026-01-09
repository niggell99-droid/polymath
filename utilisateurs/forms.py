from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil # Import du modèle Profil

# Nous étendons le formulaire d'inscription standard de Django
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Champs que l'utilisateur doit remplir lors de l'inscription
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def clean_email(self):
        # Assure que l'email est unique pour un usage professionnel
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email
    
# 1. Formulaire pour les champs du modèle User (Nom, Prénom, Email)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # On s'assure que l'email est géré comme tel

    class Meta:
        model = User
        # Champs à rendre éditables par l'utilisateur
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_username(self):
        # Optionnel : Ajouter ici une validation personnalisée du nom d'utilisateur
        username = self.cleaned_data['username']
        # Exemple de vérification si le nom d'utilisateur est déjà pris
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé par un autre compte.")
        return username

# 2. Formulaire pour les champs du modèle Profil (Bio, Avatar, Liens Sociaux)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        # Champs à rendre éditables
        fields = ['avatar', 'bio', 'site_web', 'linkedin_url']

        # Aide visuelle pour le champ bio
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }