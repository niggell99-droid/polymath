from django.contrib import admin
from .models import Topic, Thread, Post

# Pour l'affichage dans l'Admin
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'starter', 'created_at', 'is_locked', 'is_pinned')
    list_filter = ('topic', 'is_locked', 'is_pinned')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at', 'is_edited')
    list_filter = ('thread', 'author', 'is_edited')
    search_fields = ('content',)