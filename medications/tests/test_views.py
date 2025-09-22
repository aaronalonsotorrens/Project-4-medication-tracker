from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_medication_list_view(self):
        response = self.client.get(reverse('medication_list'))  # adjust the name to your actual view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medications/medication_list.html')
