from django.urls import path
from . import views

urlpatterns = [
    path('features/', views.features_list, name='features_list'),
    path('exercices/', views.exercices_list, name='exercices_list'),
    path('', views.powerbi_dashboard, name='powerbi_dashboard'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('predict/', views.predict_experience, name='predict_experience'),
    path('result/', views.result_page, name='result_page'),
]
