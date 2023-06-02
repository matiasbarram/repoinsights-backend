from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.RepoInsightsProjects.as_view(), name="get_all_projects"),
]
