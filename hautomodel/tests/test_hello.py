from django.test import TestCase

class HelloTestCase(TestCase):
    def setUp(self):
        self.HELLO = "hello"

    def test_automl_create(self):
        """Test hello"""
        self.assertEqual(self.HELLO, "hello")