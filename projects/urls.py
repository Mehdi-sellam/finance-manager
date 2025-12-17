from django.urls import path
from .views import AssignEmployeeToProjectView

urlpatterns = [
    path("assign-employee/", AssignEmployeeToProjectView.as_view(), name="assign-employee"),
]
