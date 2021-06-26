from django.test import TestCase
from hautomodel.controllers.utils_manager import Utils
from hautomodel.models import AutoMLModel

import datetime

class UtilsTestCase(TestCase):

    def setUp(self):
        AutoMLModel.objects.create(name="sd_class_model", description="test model desc", model_type="sdata_classifier", automl_backend="autosklearn", accuracy_score="", train_status='Pending', timestamp_created=datetime.datetime.now(), date_created=datetime.datetime.now(), columns=str("['col1', 'col2']"))
        AutoMLModel.objects.create(name="sd_reg_testmodel", description="test model desc", model_type="sdata_regressor", automl_backend="autosklearn", accuracy_score="", train_status='Pending', timestamp_created=datetime.datetime.now(), date_created=datetime.datetime.now(), columns=str("['col1', 'col2']"))
        AutoMLModel.objects.create(name="sd_class_model_2", description="test model desc", model_type="sdata_classifier", automl_backend="autosklearn", accuracy_score="", train_status='Pending', timestamp_created=datetime.datetime.now(), date_created=datetime.datetime.now(), columns=str("['col1', 'col2']"))

    def test_utils_get_all_sd_classifer(self):
        """Test automl create"""
        automl = Utils().get_all_sd_classifer()
        for au in automl:
            self.assertEqual(au["model_type"], "sdata_classifier")
    
    def test_utils_get_all_sd_regressor(self):
        """Test automl create"""
        automl = Utils().get_all_sd_regressor()
        for au in automl:
            self.assertEqual(au["model_type"], "sdata_regressor")
    
    def test_utils_get_all_sd(self):
        """Test automl create"""
        class_all_entries, reg_all_entries = Utils().get_all_sd()
        for c in class_all_entries:
            self.assertEqual(c["model_type"], "sdata_classifier")
        for reg in reg_all_entries:
            self.assertEqual(reg["model_type"], "sdata_regressor")
