from django.test import TestCase
from django.core.cache import cache
from django.test import Client
from rest_framework.test import APITestCase
from .models import FAQ

class FAQModelTest(TestCase):
    def setUp(self):
        cache.clear()
        
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework.",
        )
    
    def tearDown(self):
        cache.clear()

    def test_model_creation(self):
        """Test basic model creation and field values"""
        self.assertEqual(self.faq.question, "What is Django?")
        self.assertEqual(self.faq.answer, "Django is a high-level Python web framework.")
        
    def test_translation_fields_exist(self):
        """Test that translation fields are automatically created"""
        self.assertIsNotNone(self.faq.question_hi)
        self.assertIsNotNone(self.faq.question_bn)
        self.assertIsNotNone(self.faq.answer_hi)
        self.assertIsNotNone(self.faq.answer_bn)

    def test_translation_generation(self):
        """Test translation generation for both questions and answers"""
        self.assertIsNotNone(self.faq.question_hi)
        self.assertIsNotNone(self.faq.answer_hi)
        self.assertTrue(isinstance(self.faq.question_hi, str))
        self.assertTrue(isinstance(self.faq.answer_hi, str))
        
        question_hi = self.faq.get_translated_question("hi")
        answer_hi = self.faq.get_translated_answer("hi")
        
        self.assertEqual(self.faq.question_hi, question_hi)
        self.assertEqual(self.faq.answer_hi, answer_hi)

    def test_translation_caching(self):
        """Test that translations are properly cached"""
        question_hi = self.faq.get_translated_question("hi")
        answer_hi = self.faq.get_translated_answer("hi")
        
        initial_question = self.faq.question_hi
        initial_answer = self.faq.answer_hi
        
        self.assertEqual(question_hi, initial_question)
        self.assertEqual(answer_hi, initial_answer)
        
        refreshed_faq = FAQ.objects.get(id=self.faq.id)
        self.assertEqual(refreshed_faq.question_hi, initial_question)
        self.assertEqual(refreshed_faq.answer_hi, initial_answer)

    def test_invalid_language_code(self):
        """Test behavior with invalid language codes"""
        result = self.faq.get_translated_question("invalid_code")
        self.assertTrue(result is None or result == self.faq.question)

    def test_multiple_translations(self):
        """Test getting translations in multiple languages"""
        question_hi = self.faq.get_translated_question("hi")
        question_bn = self.faq.get_translated_question("bn")
        
        self.assertIsNotNone(question_hi)
        self.assertIsNotNone(question_bn)

class FAQAPITest(APITestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework.",
        )
        
    def test_faq_list_api(self):
        """Test FAQ list API endpoint"""
        url = '/api/faqs/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.faq.question)

    def test_faq_translation_api(self):
        """Test FAQ translation API endpoint"""
        url = '/api/faqs/'
        response = self.client.get(f"{url}?lang=hi")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn('question', response.data[0])