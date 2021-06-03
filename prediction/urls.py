from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.main,name="main"),
    path('result',views.Result,name="Result"),
    path('detection',views.Detection,name="Detection")
]