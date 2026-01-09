from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Modele pout les outils/technologies specifiques a l'ingenierie (ex : Arduino, CAD, Python, etc.)
class Tool(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='tool_icons/', blank=True, null=True)

    def __str__(self):
        return self.name
    
# Modele principal pour le projet / tutoriel
class Projet(models.Model):
    # Difficulte (choix predefini)
    DIFFICULTY_CHOICES = [
        ('FACILE', 'Facile'),
        ('MOYEN', 'Moyen'),
        ('DIFFICILE', 'Difficile'),
        ('EXPERT', 'Expert'),
    ]

    # Informations de base
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField(help_text="Breve description du projet.")

    # Contenu
    content = models.TextField() # Le guide ou les etapes

    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tools = models.ManyToManyField(Tool, blank=True) # Les outils / technologies utilises

    # Metadonnees
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='MOYEN')
    duration = models.CharField(max_length=50, blank=True, help_text="Ex: '4 heures' ou '2 jours'")

    # Images / Statut 
    main_image = models.ImageField(upload_to='project_images/')
    is_published = models.BooleanField(default=False)
    publication_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Nous utiliserons le nom d'URL 'projet_detail' plus tard
        return reverse('projet_detail', kwargs={'slug': self.slug})
    
    # Modele pour les etapes ou les galeries de photos (pour un projet plus visuel)
class ProjectImage(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image pour {self.projet.title}"