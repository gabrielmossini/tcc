from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'user': 'testuser', 'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'user': 'testuser', 'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensagem', response.context)