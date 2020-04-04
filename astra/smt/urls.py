"""smt URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_person_to_subsystem', views.add_person_to_subsystem),
    path('remove_assignment', views.remove_assignment),
    path('create_subsystem', views.create_subsystem),
    path('edit_subsystem', views.edit_subsystem),
    path('failed_to_contact', views.failed_to_contact),
]
