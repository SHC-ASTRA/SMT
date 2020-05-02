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
    path('archive', views.archive_subsystem),
    path('failed_to_contact', views.failed_to_contact),
    path('gen_person_data', views.gen_person_data),
    path('gen_subsystem_data', views.gen_subsystem_data),
]
