from django.urls import path
from .views import GithubLogin, GithubCallback, RegularLogin

urlpatterns = [
    path("login/github/", GithubLogin.as_view(), name="github_login"),
    path("login/", RegularLogin.as_view(), name="regular_login"),
    path("github/callback/", GithubCallback.as_view(), name="github_callback")
]
