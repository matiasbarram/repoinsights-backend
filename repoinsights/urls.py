from django.urls import path
from . import views


urlpatterns = [
    path("projects/", views.RepoInsightsProjects.as_view(), name="get_all_projects"),
    path("filters/langs/", views.RepoInsightsProjectsLangs.as_view(), name="get_all_projects_langs"),
    path("explore/", views.RepoInsightsExplore.as_view(), name="explore_projects"),
]
