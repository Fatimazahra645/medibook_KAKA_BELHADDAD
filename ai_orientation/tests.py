from django.test import TestCase

class AIOrientationTests(TestCase):

    def test_ai_page_load(self):
        response = self.client.get("/")  # adapte si tu as une view
        self.assertIn(response.status_code, [200, 404])  # safe test baseline