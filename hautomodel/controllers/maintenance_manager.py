from ..models import AutoMLModel

import os

class MaintenanceMan():
    def run_maintenance(self):
        automl_data = [au.name for au in AutoMLModel.objects.all()]
        pkl_models =  [name.split(".")[0] for name in os.listdir('./hautomodel/automl_pkl_models/')]

        # DELETE PICKLE FILES IF NOT IN DJANGO MODEL
        for pkl in pkl_models:
            if pkl not in automl_data:
                try:         
                    os.remove('./hautomodel/automl_pkl_models/'+pkl+".pkl")
                except Exception as e:
                    print("Error deleting model {} : ".format(pkl+".pkl"), e)
        
        # DELETED DJANGO MODEL IF NOT IN PICKLE FILES
        for automl in automl_data:
            if automl not in pkl_models:
                AutoMLModel.objects.filter(name=automl).delete()
        return True