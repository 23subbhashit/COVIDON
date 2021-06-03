from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.main,name="main"),
    path('predict',views.Predict,name="Predict"),
    path('detection',views.Detection,name="Detection"),
    path('predictionresult',views.PredictionResult,name="PredictionResult")
    
]