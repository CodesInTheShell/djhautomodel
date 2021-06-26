from django.urls import path, include
from django.contrib import admin
from rest_framework.authtoken import views as drf_views
from rest_framework import routers

from . import views
from . import views_api
from .controllers.auth_manager import CustomAuthToken

admin.site.site_header = 'Hautomodel'
admin.site.index_title = 'Welcome to Hautomodel Admin Panel' 
admin.site.site_title = 'Hautomodel'

router = routers.DefaultRouter()
router.register('automlmodel', views_api.AutoMLViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('struc_data_classifier/', views.struc_data_classifier, name='struc_data_classifier'),
    path('struc_data_regressor/', views.struc_data_regressor, name='struc_data_regressor'),
    path('train_new/', views.train_new, name='train_new'),
    path('logout_hautomodel/', views.logout_hautomodel, name='logout_hautomodel'),
    path('sd_predict/<str:model_name>/', views.sd_predict, name='sd_predict'),
    path('contact_dev/', views.contact_dev, name='contact_dev'),
    path('faqs/', views.faqs, name='faqs'),
    path('maintenance/', views.maintenance, name='maintenance'),
    ### API VIEWS
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('api/train_sd/', views_api.TrainSD.as_view(), name='api_train_sd'),
    path('api/predict_sd/', views_api.PredictSD.as_view(), name='api_predict_sd'),
    path('api/', include(router.urls))
]

# SHOW STATIC FILES USING GUNICORN
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()