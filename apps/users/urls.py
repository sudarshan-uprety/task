from django.urls import path

from apps.users import views


urlpatterns = [
    path("register", views.UserRegistrationView.as_view(), name="user_registration"),
    path("login", views.UserLogin.as_view(), name="user_login"),
    path("refresh/token", views.UserRefreshTokenView.as_view(), name="user_refresh_token"),

]
