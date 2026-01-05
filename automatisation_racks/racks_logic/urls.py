from django.urls import path

from automatisation_racks.racks_logic import views

urlpatterns = [
    path("", views.racks_logic, name="racks-logic"),
]