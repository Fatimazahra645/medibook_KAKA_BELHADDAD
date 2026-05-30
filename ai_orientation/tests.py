from django.test import TestCase
from .services import suggest_speciality


class AIOrientationTests(TestCase):

    def test_suggest_cardiologie(self):
        results = suggest_speciality("douleur poitrine palpitation essoufflement")
        self.assertEqual(results[0]["speciality"], "Cardiologie")

    def test_suggest_dermatologie(self):
        results = suggest_speciality("boutons peau rougeur démangeaison")
        self.assertEqual(results[0]["speciality"], "Dermatologie")

    def test_suggest_dentisterie(self):
        results = suggest_speciality("douleur dent carie gencive")
        self.assertEqual(results[0]["speciality"], "Dentisterie")

    def test_suggest_returns_list(self):
        results = suggest_speciality("mal à la tête et fatigue")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("speciality", results[0])
        self.assertIn("score", results[0])

    def test_suggest_empty_text_returns_default(self):
        results = suggest_speciality("")
        self.assertEqual(results[0]["speciality"], "Médecine générale")

    def test_ai_page_loads(self):
        response = self.client.get("/ai/")
        self.assertEqual(response.status_code, 200)
