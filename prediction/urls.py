from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('maskdetect', views.index, name='index'),

    #access the laptop camera
    path('video_feed', views.video_feed, name='video_feed'),
    path('',views.main,name="main"),
    path('predict',views.Predict,name="Predict"),
    path('about',views.Prevention,name="Prevention"),
    path('predictionresult',views.PredictionResult,name="PredictionResult"),
    path('news',views.News,name="News"),
    path('vaccinedetails',views.vaccine,name="Vaccine")
    
]