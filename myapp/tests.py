from django.test import TestCase
from django.urls import reverse
# Create your tests here.


class HelloWorldTemplateTests(TestCase):
    def test_hello_world_template(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello_world.html')
        self.assertContains(response, "Hello, World!")