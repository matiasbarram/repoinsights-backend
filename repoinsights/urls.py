from django.urls import path
from . import views


urlpatterns = [
    path("projects/", views.RepoInsightsProjects.as_view(), name="get_all_projects"),
    path("filters/", views.RepoInsightsProjectsFilters.as_view(), name="get_all_projects_filters"),
    path("explore/", views.RepoInsightsExplore.as_view(), name="explore_projects"),
]
