from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Topic, Thread


class ForumPaginationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='forumuser', password='pass')
        self.topic = Topic.objects.create(name='Tech', slug='tech', description='desc')

        # Create 12 threads
        for i in range(12):
            Thread.objects.create(
                title=f'Thread {i}',
                slug=f'thread-{i}',
                topic=self.topic,
                starter=self.user
            )

    def test_topic_detail_pagination_first_page(self):
        # Vérifier que la pagination retourne bien 10 threads par page
        from django.core.paginator import Paginator
        threads_qs = Thread.objects.filter(topic=self.topic)
        paginator = Paginator(threads_qs, 10)
        page1 = paginator.page(1)
        self.assertEqual(len(page1.object_list), 10)

    def test_topic_detail_pagination_second_page(self):
        # Vérifier que la pagination retourne bien 2 threads sur la deuxième page
        from django.core.paginator import Paginator
        threads_qs = Thread.objects.filter(topic=self.topic)
        paginator = Paginator(threads_qs, 10)
        page2 = paginator.page(2)
        self.assertEqual(len(page2.object_list), 2)