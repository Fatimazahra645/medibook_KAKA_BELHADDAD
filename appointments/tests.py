from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AppointmentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="patient1",
            password="testpass123"
        )

    def test_user_authenticated_can_access(self):
        self.client.login(username="patient1", password="testpass123")
        response = self.client.get("/")  # adapte selon ta view appointments
        self.assertIn(response.status_code, [200, 302])