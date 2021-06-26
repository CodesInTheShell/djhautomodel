from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import AutoMLModel

import os
import pandas
import pickle
import numpy as np
import json
import threading
import ast

from .controllers.printer_man import ManagerPrinter
from .controllers.train_manager import SDTrainStartManager
from .controllers.predict_manager import SDPredictStartManager
from .controllers.utils_manager import Utils
from .controllers.maintenance_manager import MaintenanceMan


def index(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user) # USE if request.user.is_authenticated: to check user in other views or use @login_required(login_url='/')
            return redirect('dashboard')
        else:
            context = {}
            return render(request, "index.html", context)              
    else:
        ManagerPrinter().printer()
        context = {}

        # IF ALREADY LOGGED IN SESSION
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, "index.html", context)

def logout_hautomodel(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/')
def dashboard(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()    
    all_sd_class = Utils().get_all_sd_classifer()
    all_sd_reg = Utils().get_all_sd_regressor()

    stats = {
        "sd_class_count": str(len(all_sd_class)),
        "sd_reg_count": str(len(all_sd_reg))
    }

    context = { "user": user["username"], "stats": stats}
    return render(request, "dashboard.html", context) 

@login_required(login_url='/')
def settings(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
    context = { "user": user["username"]}
    return render(request, "settings.html", context)

@login_required(login_url='/')
def contact_dev(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
    context = { "user": user["username"]}
    return render(request, "contact_dev.html", context) 

@login_required(login_url='/')
def faqs(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
    context = { "user": user["username"]}
    return render(request, "faqs.html", context) 
            
@login_required(login_url='/')
def struc_data_classifier(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
    all_entries = AutoMLModel.objects.filter(model_type='sdata_classifier')

    context = { 
        "user": user["username"],
        "automl_entries": all_entries.values(),
        }
    return render(request, "struc_data_classifier.html", context)

@login_required(login_url='/')
def struc_data_regressor(request):
    context = {}
    user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
    all_entries = AutoMLModel.objects.filter(model_type='sdata_regressor')

    context = { 
        "user": user["username"],
        "automl_entries": all_entries.values(),
        }
    return render(request, "struc_data_regressor.html", context)

@login_required(login_url='/')
def train_new(request):
    if request.method == 'POST':
        result = request.POST.dict()
        modelname = result['modelname_input']
        targetname = result['targetname_input']
        model_desc = result['description_textarea']
        traning_time = int(result['train_time_input']) * 60
        model_type = result['model_type_radio']
        automl_vendor = result['automl_vendor']
        request.FILES['file']
        try: 
            df = pandas.read_csv(request.FILES['file'])
        except pandas.errors.EmptyDataError:
            print("errors")
            return redirect('train_new')
        t1 = threading.Thread(target=SDTrainStartManager().start_training, args=(targetname, df, modelname, model_desc, traning_time, model_type, automl_vendor))
        t1.start()
        return redirect('dashboard')
    else:
        context = {}
        user = request.user.__class__.objects.filter(pk=request.user.id).values().first()
        context = { "user": user["username"]}
        return render(request, "train_new.html", context)

@login_required(login_url='/')
def sd_predict(request, model_name):

    if request.method == "POST":

        # IF SINGLE PREDICTION
        if len(request.FILES) == 0:
            automl_data, predictors, pred_class, pred_proba = SDPredictStartManager().single_prediction(model_name, request)
            context = {"automl_data": automl_data, "predictors": predictors, "pred_class": pred_class, "pred_proba": pred_proba}
            return render(request, "sd_predict.html", context)

        # IF CSV PREDICTION
        csv_dataset = request.FILES['csv_dataset']
        try:
            dataset = pandas.read_csv(csv_dataset)
        except Exception as e:
            print('Error: ', e)
            return redirect('sd_predict')

        # dataset = pandas.DataFrame.from_dict(json.loads(dataset.to_json()))

        # with open('./hautomodel/automl_pkl_models/'+'{}.pkl'.format(model_name), 'rb') as f:
        #     automl = pickle.load(f)

        # pred_and_proba = SDPredictStartManager().start_predict_dataset(automl, dataset)
        # df = pandas.DataFrame(pred_and_proba, columns=['Predicted', 'Probability'])

        df = SDPredictStartManager().csv_prediction(dataset, model_name)
        df.to_csv()
        response = HttpResponse(df.to_csv(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=result.csv'
        return response
         
    else:
        automl_data = AutoMLModel.objects.filter(name=model_name).values()[0]        
        predictors = ast.literal_eval(automl_data["columns"])
        context = {"automl_data": automl_data, "predictors": predictors}
        return render(request, "sd_predict.html", context)

@login_required(login_url='/')
def maintenance(request):
    res = MaintenanceMan().run_maintenance()
    return redirect('dashboard')