from django.urls import path
from repoinsights.views.explore import RepoInsightsExplore
from repoinsights.views.filters import RepoInsightsProjectsFilters
from repoinsights.views.projects import RepoInsightsProjects
from repoinsights.views.featured import RepoInsightsFeaturedProjects

urlpatterns = [
    path("projects/", RepoInsightsProjects.as_view(), name="get_all_projects"),
    path("filters/", RepoInsightsProjectsFilters.as_view(), name="get_all_projects_filters"),
    path("explore/", RepoInsightsExplore.as_view(), name="explore_projects"),
    path("explore/featured/", RepoInsightsFeaturedProjects.as_view(), name="explore_featured_projects"),
]
