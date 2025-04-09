from django.urls import path
from . import views

urlpatterns = [
    path('add-meal/', views.add_meal, name='add_meal'),
]