from django.test import TestCase
from django.urls import reverse

class DoctorsTests(TestCase):

    def test_doctors_page_loads(self):
        response = self.client.get(reverse("doctors"))
        self.assertEqual(response.status_code, 200)