from sklearn.preprocessing import LabelEncoder
import autosklearn.classification
import autosklearn.regression
import sklearn.model_selection
from sklearn.metrics import r2_score
import numpy as np
from django.core.files.storage import default_storage

from ..models import AutoMLModel

from datetime import datetime
import pickle
import os
import csv
import pandas
import json


class SDTrainStartManager():
    """Manage training contexts."""

    def start_training(self, targetname, df, modelname, model_desc, traning_time, model_type, automl_backend="autosklearn"):
        """
        Run the training

        :param targetname: (str) The column field name of the target.
        :param df: (dataframe) Dataframe to use for training.
        :param modelname: (str) Model name to create after this training.
        :param model_desc: (str) Model description.
        :param training_time: (int) Training time in minutes to run the training.
        :param model_type: (str) classifier or regressor.

        :return status: accuracy, etc 
        """

        status = {}

        self.modelname = modelname
        self.df = df 
        self.target_df = df[targetname]
        self.inputs_df = self.df.drop(targetname, axis='columns')
        self.model_desc = model_desc
        self.traning_time = int(traning_time)
        self.model_type = model_type
        self.automl_backend = automl_backend

        columns_txt = [c for c in self.inputs_df.columns]

        # CREATE AUTOML MODEL IN DATABASE WITH STATUS "pending"
        ml = AutoMLModel(name=self.modelname, description=self.model_desc, model_type=self.model_type, automl_backend=automl_backend, accuracy_score="", train_status='Pending', timestamp_created=datetime.now(), date_created=datetime.now(), columns=str(columns_txt))
        ml.save()

        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(self.inputs_df, self.target_df, random_state=1)

        if self.model_type == 'sdata_classifier':
            automl = autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=self.traning_time)
            automl.fit(X_train, y_train)
            y_hat = automl.predict(X_test)
            accuracy_score = str(sklearn.metrics.accuracy_score(y_test, y_hat))
        else:
            automl = autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=self.traning_time)
            automl.fit(X_train, y_train)
            y_hat = automl.predict(X_test)
            accuracy_score = str(r2_score(y_test, y_hat))

        with open('./hautomodel/automl_pkl_models/'+'{}.pkl'.format(self.modelname), 'wb') as f:
            pickle.dump(automl, f)
        
        accuracy_score = "{:.2f}".format(float(accuracy_score))

        status['status'] = 'Success'
        status['message'] = 'Model has been created'
        status['accuracy_score'] = accuracy_score
        status['modelname'] =self.modelname
        print("regressor status: ", status )

        AutoMLModel.objects.filter(name=self.modelname).update(accuracy_score=accuracy_score)
        AutoMLModel.objects.filter(name=self.modelname).update(train_status="Completed")

        return status

        
