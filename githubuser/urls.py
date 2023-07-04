from django.urls import path, include
from .views.views import GitHubProjects, UserTokens, GitHubAddProject, UserAddTokens
from .views.contribute.project import GitHubContribute

urlpatterns = [
    path("projects/", GitHubProjects.as_view(), name="github_projects"),
    path("projects/add", GitHubAddProject.as_view(), name="github_projects_add"),
    path("contribute/", GitHubContribute.as_view(), name="github_contribute"),
    path("tokens/", UserTokens.as_view(), name="github_token"),
    path("tokens/add", UserAddTokens.as_view(), name="github_token_add")
]
