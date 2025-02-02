from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.core.cache import cache

translator = Translator()

class FAQ(models.Model):
    LANGUAGES = [("en", "English"), ("hi", "Hindi"), ("bn", "Bengali")]

    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-translate using Google Translate API
        if not self.question_hi:
            self.question_hi = translator.translate(self.question, src="en", dest="hi").text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question, src="en", dest="bn").text
        if not self.answer_hi:
            self.answer_hi = translator.translate(self.answer, src="en", dest="hi").text
        if not self.answer_bn:
            self.answer_bn = translator.translate(self.answer, src="en", dest="bn").text
        super().save(*args, **kwargs)

    def get_translated_question(self, lang):
        cache_key = f"faq_{self.id}_{lang}"
        cached_value = cache.get(cache_key)

        if cached_value:
            return cached_value

        if lang == "hi":
            translation = self.question_hi or self.question
        elif lang == "bn":
            translation = self.question_bn or self.question
        else:
            translation = self.question

        cache.set(cache_key, translation, timeout=3600)  # Cache for 1 hour
        return translation

    def get_translated_answer(self, lang):
        cache_key = f"faq_{self.id}_{lang}_answer"
        cached_value = cache.get(cache_key)

        if cached_value:
            return cached_value

        if lang == "hi":
            translation = self.answer_hi or self.answer
        elif lang == "bn":
            translation = self.answer_bn or self.answer
        else:
            translation = self.answer

        cache.set(cache_key, translation, timeout=3600)  # Cache for 1 hour
        return translation

    def __str__(self):
        return self.question
