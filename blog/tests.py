from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Article, Category


class BlogPaginationTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='tester', password='pass')
		self.category = Category.objects.create(name='Test', slug='test')

		# Create 15 published articles
		for i in range(15):
			Article.objects.create(
				title=f'Article {i}',
				slug=f'article-{i}',
				excerpt='ex',
				content='contenu',
				author=self.user,
				category=self.category,
				publication_date=timezone.now(),
				is_published=True
			)

	def test_article_list_pagination_first_page(self):
		url = reverse('blog:article_list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		articles = response.context['articles']
		# Should be a Page object with 10 items on first page
		self.assertEqual(len(articles.object_list), 10)

	def test_article_list_pagination_second_page(self):
		url = reverse('blog:article_list') + '?page=2'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		articles = response.context['articles']
		# Remaining 5 articles on second page
		self.assertEqual(len(articles.object_list), 5)
