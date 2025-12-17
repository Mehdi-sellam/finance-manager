from django.urls import path
from .views import AssignEmployeeView

urlpatterns = [
    path("assign-employee/", AssignEmployeeView.as_view(), name="assign-employee"),
]
