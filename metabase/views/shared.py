from rest_framework.views import APIView
from django.http import JsonResponse

from .connector.metabase_conn import MetabaseClient


class SharedDashboard(APIView):
    def post(self, request):
        user_id = request.user.id
        client = MetabaseClient()
        dashboards_ids = client.dashboard.get_dashboard_ids("shared")
        iframes = []
        for dash_id in dashboards_ids:
            iframe, params = client.share.create_iframe_url(user_id, dash_id, None)
            iframes.append({"iframe": iframe, "params": params})
        return JsonResponse({"dashboards": iframes}, safe=True)