from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTests(TestCase):

    def setUp(self):
        self.client = Client()

    # -------------------------
    # TEST REGISTER
    # -------------------------
    def test_register_user(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser",
            "password": "testpass123",
        })

        # vérifier redirection vers login
        self.assertEqual(response.status_code, 302)

        # vérifier que l'utilisateur existe en base
        self.assertTrue(User.objects.filter(username="testuser").exists())


    # -------------------------
    # TEST LOGIN SUCCESS
    # -------------------------
    def test_login_user(self):
        # créer utilisateur
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123",
        })

        # login réussi → redirection vers home
        self.assertEqual(response.status_code, 302)


    # -------------------------
    # TEST HOME PAGE
    # -------------------------
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)