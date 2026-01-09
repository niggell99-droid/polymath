from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profil

# 1. Définir l'édition du Profil comme "Inline"
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profil'

# 2. Étendre l'interface Admin User de Django
class UserAdmin(BaseUserAdmin):
    inlines = (ProfilInline,)
    list_display = BaseUserAdmin.list_display + ('is_author',) # Ajoute is_author à la liste

    def is_author(self, obj):
        # Fonction pour afficher le statut 'is_author' dans la liste des utilisateurs
        # Si un profil existe, affiche son statut
        return obj.profil.is_author if hasattr(obj, 'profil') else False
    is_author.boolean = True # Affiche une icône verte/rouge

# 3. Désenregistrer le modèle User original, puis l'enregistrer avec notre personnalisation
admin.site.unregister(User)
admin.site.register(User, UserAdmin)