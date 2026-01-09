from django import forms
from .models import Comment, NewsletterSubscription

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 3, 
                'placeholder': 'Partagez votre avis (respectueux et constructif)...'
            }),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com'
            })
        }
