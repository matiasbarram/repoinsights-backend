from django.urls import path
from .views.dashboards import MetabaseDashboards

urlpatterns = [
    path("public/dashboards/", MetabaseDashboards.as_view(), name="metabase_dashboard"),
]
