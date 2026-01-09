from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 1. Thème (Topic) : La catégorie principale du forum
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # URL de la liste des sujets d'un thème
        return reverse('topic_detail', kwargs={'slug': self.slug})


# 2. Sujet (Thread) : Le fil de discussion initié par un utilisateur
class Thread(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='threads')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads') # L'utilisateur qui a créé le sujet

    views = models.IntegerField(default=0) # Compteur de vues (pour la popularité)
    is_locked = models.BooleanField(default=False) # Si le sujet est fermé aux réponses
    is_pinned = models.BooleanField(default=False) # Si le sujet doit rester en haut de la liste

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at'] # Affiche les sujets épinglés en premier, puis les plus récents

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # URL du sujet spécifique
        return reverse('thread_detail', kwargs={'topic_slug': self.topic.slug, 'thread_slug': self.slug})

# 3. Message (Post) : Les réponses au sein d'un Sujet
class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at'] # Les messages sont affichés par ordre chronologique

    def __str__(self):
        # Retourne les 50 premiers caractères du message pour l'Admin
        return f"Post par {self.author.username} dans '{self.thread.title}'"[:50]