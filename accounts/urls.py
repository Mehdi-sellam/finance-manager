from django.urls import path
from .views import ChangePasseordView, CreateUserView, LoginView

urlpatterns = [
    path("create-user/", CreateUserView.as_view()),
    path("change-password/", ChangePasseordView.as_view()),
    path("login/", LoginView.as_view()),
]
