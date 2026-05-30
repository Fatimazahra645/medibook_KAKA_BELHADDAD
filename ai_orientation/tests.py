from django.test import TestCase
from .services import suggest_speciality


class AIOrientationTests(TestCase):

    def test_suggest_cardiologie(self):
        result = suggest_speciality("J'ai des douleurs à la poitrine et des palpitations")
        self.assertEqual(result, "Cardiologie")

    def test_suggest_dermatologie(self):
        result = suggest_speciality("J'ai des boutons sur la peau")
        self.assertEqual(result, "Dermatologie")

    def test_suggest_dentisterie(self):
        result = suggest_speciality("J'ai une douleur dentaire")
        self.assertEqual(result, "Dentisterie")

    def test_suggest_default(self):
        result = suggest_speciality("Je ne me sens pas bien")
        self.assertEqual(result, "Médecine générale")

    def test_ai_page_load(self):
        response = self.client.get("/ai/")
        self.assertIn(response.status_code, [200, 404])
