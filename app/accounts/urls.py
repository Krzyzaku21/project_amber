from . import views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path("register_panel/", views.RegisterAPI.as_view(), name="register_panel"),
    path("email_verifi/<token>/", views.EmailVerifiAPI.as_view(), name="register_email_response"),
    path("login_panel/", views.LoginAPI.as_view(), name="login_panel"),
]
