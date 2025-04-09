from django.urls import path
from . import views

urlpatterns = [
    path('add-meal/', views.add_meal, name='add_meal'),
    path('records/', views.records, name='records'),
    path('add-food-item/', views.add_food_item, name='add_food_item'),
    path('delete-record/<int:record_id>/', views.delete_record, name='delete_record'),
]