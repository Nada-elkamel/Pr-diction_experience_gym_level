from django.urls import path
from . import views

urlpatterns = [
    path('features/', views.features_list, name='features_list'),
    path('exercices/', views.exercices_list, name='exercices_list'),
    path('dashboard/', views.powerbi_dashboard, name='powerbi_dashboard'),

]
