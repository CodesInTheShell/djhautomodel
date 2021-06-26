import numpy as np
from ..models import AutoMLModel

import ast
import pickle
import pandas
import json

class SDPredictStartManager():
    """Manage prediction contexts."""

    def start_predict_dataset(self, model, dataset):
        """
        Batch prediction from a dataset.

        :param model: Model object from pickle.
        :param dataset: Pandas dataset to run prediction. 

        :return pred_and_proba: List of list pair of predicted class and probabilities.
        """

        pred = model.predict(dataset).tolist()

        try:
            proba = (np.amax(model.predict_proba(dataset), axis=1)).tolist()
        except AttributeError as error:
            print(str(error))
            proba = ['na' for i in range(len(pred))]

        pred_and_proba = [list(a) for a in zip(pred, proba)]   
        return pred_and_proba
    
    def single_prediction(self, model_name, request):

        automl_data = AutoMLModel.objects.filter(name=model_name).values()[0]        
        predictors = ast.literal_eval(automl_data["columns"])
        result = request.POST.dict()
        dataset = []
        for p in predictors:
            dataset.append(int(result[p]))
        new_data = np.array([dataset])
        with open('./hautomodel/automl_pkl_models/'+'{}.pkl'.format(model_name), 'rb') as f:
            automl = pickle.load(f)
        pred_and_proba = self.start_predict_dataset(automl, new_data)
        pred_and_proba = list(pred_and_proba)[0]
        pred_class = pred_and_proba[0]
        try:
            pred_proba = "{:.2f}".format(float(pred_and_proba[1]))
        except Exception as e:
            pred_proba = pred_and_proba[1]
        
        return automl_data, predictors, pred_class, pred_proba
    
    def csv_prediction(self, dataset, model_name):        
        dataset = pandas.DataFrame.from_dict(json.loads(dataset.to_json()))
        with open('./hautomodel/automl_pkl_models/'+'{}.pkl'.format(model_name), 'rb') as f:
            automl = pickle.load(f)
        pred_and_proba = self.start_predict_dataset(automl, dataset)
        df = pandas.DataFrame(pred_and_proba, columns=['Predicted', 'Probability'])
        return df
    
    def api_prediction(self, dataset, model_name):
        with open('./hautomodel/automl_pkl_models/'+'{}.pkl'.format(model_name), 'rb') as f:
            automl = pickle.load(f)
        pred_and_proba = self.start_predict_dataset(automl, dataset)
        return pred_and_proba