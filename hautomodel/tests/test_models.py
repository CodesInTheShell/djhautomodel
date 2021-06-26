from django.test import TestCase
from hautomodel.models import AutoMLModel

import datetime

class AutoMLModelTestCase(TestCase):
    def setUp(self):
        AutoMLModel.objects.create(name="testmodel", description="test model desc", model_type="sdata_classifier", automl_backend="autosklearn", accuracy_score="", train_status='Pending', timestamp_created=datetime.datetime.now(), date_created=datetime.datetime.now(), columns=str("['col1', 'col2']"))

    def test_automl_create(self):
        """Test automl create"""
        automl = AutoMLModel.objects.filter(name="testmodel")[0]
        self.assertEqual(automl.name, "testmodel")
        self.assertEqual(automl.model_type, "sdata_classifier")