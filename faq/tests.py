from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import FAQ

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework.",
        )

    def test_translation(self):
        self.assertTrue(self.faq.question_hi)
        self.assertTrue(self.faq.question_bn)
        self.assertTrue(self.faq.answer_hi)
        self.assertTrue(self.faq.answer_bn)

    def test_cached_translation(self):
        cached_question = self.faq.get_translated_question("hi")
        cached_answer = self.faq.get_translated_answer("hi")
        self.assertEqual(cached_question, self.faq.question_hi)
        self.assertEqual(cached_answer, self.faq.answer_hi)



class FAQAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework.",
        )

    def test_faq_list_default_language(self):
        """Test FAQ list API without language parameter (defaults to English)."""
        response = self.client.get(reverse("faq-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["question"], "What is Django?")

    def test_faq_list_with_language_parameter(self):
        """Test FAQ list API with language parameter (?lang=hi)."""
        response = self.client.get(reverse("faq-list"), {"lang": "hi"})
        self.assertEqual(response.status_code, 200)
        print(response.data[0]["question"])
        self.assertEqual(response.data[0]["question"], self.faq.question_hi)

    def test_faq_list_invalid_language(self):
        """Test fallback to English if an unsupported language is requested."""
        response = self.client.get(reverse("faq-list"), {"lang": "fr"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["question"], "What is Django?")
