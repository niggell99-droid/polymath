# articles/admin.py
from django.contrib import admin
from .models import Article, Category, Tag

# Enregistrement des modèles simples
admin.site.register(Category)
admin.site.register(Tag)

# Enregistrement du modèle Article avec personnalisation pour plus de professionnalisme
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date', 'is_published')
    list_filter = ('category', 'tags', 'is_published')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)} # Remplissage automatique du slug à partir du titre
    date_hierarchy = 'publication_date'

    # Fieldsets (organisation des champs dans la page d'edition)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content')
        }),
        ('Publication & Visibilite', {
            'fields': ('is_published', 'publication_date', 'featured_image', 'reading_time', 'video_status'),
            'classes': ('collapse',),
        })
    )
