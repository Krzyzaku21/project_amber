from .accounts_serializers import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path("api_register/", views.api_register, name="api_register"),
]
