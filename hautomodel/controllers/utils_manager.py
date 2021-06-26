from ..models import AutoMLModel

class Utils():

    def get_all_sd_classifer(self):
        all_entries = AutoMLModel.objects.filter(model_type='sdata_classifier')
        return all_entries.values()

    def get_all_sd_regressor(self):
        all_entries = AutoMLModel.objects.filter(model_type='sdata_regressor')
        return all_entries.values()

    def get_all_sd(self):
        class_all_entries = self.get_all_sd_classifer()
        reg_all_entries = self.get_all_sd_regressor()

        return class_all_entries, reg_all_entries

        

