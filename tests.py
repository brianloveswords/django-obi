from django.test import TestCase
from django.conf import settings

class BasicTests(TestCase):
    def test_valid_settings(self):
        self.assertTrue(False, "Cheap failing test")
