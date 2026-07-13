"""URLs de habits: listar, crear, toggle, eliminar."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.habito_list, name='habito_list'),
    path('crear/', views.habito_create, name='habito_create'),
    path('<int:pk>/toggle/', views.habito_toggle, name='habito_toggle'),
    path('<int:pk>/eliminar/', views.habito_delete, name='habito_delete'),
]
