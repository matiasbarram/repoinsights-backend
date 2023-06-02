from django.urls import path, include
from .views import GitHubProjects, UserTokens, GitHubAddProject, UserAddTokens

urlpatterns = [
    path("projects/", GitHubProjects.as_view(), name="github_projects"),
    path("projects/add", GitHubAddProject.as_view(), name="github_projects_add"),    
    path("tokens/", UserTokens.as_view(), name="github_token"),
    path("tokens/add", UserAddTokens.as_view(), name="github_token_add")
]
