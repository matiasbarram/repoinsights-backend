from django.urls import path
from .views.dashboards import MetabaseDashboards
from .views.single import SingleDashboard, SingleDashboardByID
from .views.shared import SharedDashboard

urlpatterns = [
    path("public/dashboards/", MetabaseDashboards.as_view(), name="metabase_dashboard"),
    path("public/dashboards/single/", SingleDashboard.as_view(), name="metabase__single_dashboard"),
    path("public/dashboards/shared/", SharedDashboard.as_view(), name="metabase_shared_dashboard"),
    path("public/dashboards/<int:dashboard_id>/", SingleDashboardByID.as_view(), name="metabase_dashboard"),
]
