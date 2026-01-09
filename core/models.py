from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EmailValidator

class NewsletterSubscription(models.Model):
    """Model for newsletter email subscriptions"""
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Email address for newsletter subscription"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
    
    def __str__(self):
        return f"{self.email} - {'Active' if self.is_active else 'Inactive'}"

class Comment(models.Model):
    """
    Generic comment model that can be attached to any other model 
    (Articles, Projects, etc.)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif") # For moderation
    
    # Generic Foreign Key configuration
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['created_at'] # Chronological order
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object}"
