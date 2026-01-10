from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Article, Category
from django.contrib.auth.models import User

class CoreIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        
    def test_homepage_loads(self):
        """Test that the homepage loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        
    def test_search_page_loads(self):
        """Test that the search page loads"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search_results.html')

    def test_legal_pages_load(self):
        """Test that legal pages load"""
        legal_urls = ['legal', 'privacy', 'terms', 'contact']
        for url_name in legal_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, f"{url_name} failed to load")
