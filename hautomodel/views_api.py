from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from .controllers.auth_manager import ExpiringTokenAuthentication
from .controllers.train_manager import SDTrainStartManager
from .controllers.predict_manager import SDPredictStartManager
from .models import AutoMLModel
from .serializer import AutomlSerializer

import pandas
import threading

class AutoMLViewSet(mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    AutoML Models queryset GET, PUT, DELETE methods.
    
    Example: 
    GET http://localhost:8000/api/automlmodel/
    DELETE http://localhost:8000/api/automlmodel/7/
    
    Please refer to drf routers for more usage:
    https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    """

    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = AutoMLModel.objects.all()
    serializer_class = AutomlSerializer


class TrainSD(APIView):
    """
    Train structured data classifier or regressor

    EXAMPLE:
    {
    "modelname": "graduated",
    "targetname": "graduated",
    "model_desc": "graduated4 model_desc",
    "traning_time": "60",
    "model_type": "sdata_classifier",
    "automl_backend": "autosklearn", #optional
    "dataset": { the dataset in dict include head title } 
    """
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):        
        result = request.data
        modelname = result['modelname']
        targetname = result['targetname']
        model_desc = result['model_desc']
        traning_time = int(result['traning_time']) * 60
        model_type = result['model_type']
        automl_backend = result.get('automl_backend', 'autosklearn')
        df = result['dataset']

        if automl_backend != 'autosklearn':
            return Response({'message': 'Currently supports only autosklearn'})
        
        try: 
            df = pandas.DataFrame.from_dict(df)
        except pandas.errors.EmptyDataError:
            print("errors")
            content = {'message': 'Error in training dataset'}
            return Response(content)

        t1 = threading.Thread(target=SDTrainStartManager().start_training, args=(targetname, df, modelname, model_desc, traning_time, model_type, automl_backend,))
        t1.start()

        content = {'message': 'Started training for {} model.'.format(modelname)}
        return Response(content)

class PredictSD(APIView):
    """
    Predict structured data classifier or regressor

    {
    "modelname": "graduatedapi1",
    "automl_backend": "autosklearn", #optional
    "dataset": { the dataset in dict include head title } 
    """

    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        result = request.data
        modelname = result['modelname']
        automl_backend = result.get('automl_backend', 'autosklearn')
        df = result['dataset']

        if automl_backend != 'autosklearn':
            return Response({'message': 'Currently supports only autosklearn'})

        try: 
            df = pandas.DataFrame.from_dict(df)
        except pandas.errors.EmptyDataError:
            print("errors")
            content = {'message': 'Error in predict dataset'}
            return Response(content)
        
        pred_and_proba = SDPredictStartManager().api_prediction(df, modelname)
        status={}
        status['status'] = 'Success'
        status['predictions'] = pred_and_proba
        return Response(status)