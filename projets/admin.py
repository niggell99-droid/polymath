from django.contrib import admin
from .models import Projet, Tool, ProjectImage

# Pour gerer la galerie d'images directement dans le formulaire du Projet (plus pratique)
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1 # Nombre de formulaires vides a afficher par defaut

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'is_published', 'publication_date')
    list_filter = ('difficulty', 'is_published', 'tools')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline] # Integre la gestion des images
    date_hierarchy = 'publication_date'

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)