from django.urls import path
from .views.dashboards import ProtectedView, MetabaseDashboards

urlpatterns = [
    path("test/", ProtectedView.as_view(), name="test"),
    path("public/dashboards/", MetabaseDashboards.as_view(), name="metabase_dashboard"),
]
