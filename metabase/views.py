from pprint import pprint
from typing import Any, Tuple
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
import time
from django.conf import settings



class ProtectedView(APIView):
    def get(self, request):
        return Response(
            {"message": "Esta información es solo para usuarios autenticados"}
        )


class MetabaseDashboards(APIView):
    def __init__(self) -> None:
        self.METABASE_SITE_URL = settings.METABASE_URL
        self.METABASE_SECRET_KEY = settings.METABASE_SECRET_KEY

    def get_token(self, payload):
        return jwt.encode(payload, self.METABASE_SECRET_KEY, algorithm="HS256")

    def get_ids(self):
        # call api
        return ["3", "4", "5"]

    def create_iframe_url(self, dashboard_id, params) -> Tuple:
        if params is None:
            params = {"id": ["1", "2", "3", "4"]}
        payload = {
            "resource": {"dashboard": int(dashboard_id)},
            "params": params,
            "exp": round(time.time()) + (60 * 10),  # 10 minute expiration
        }

        iframeUrl = (
            self.METABASE_SITE_URL
            + "/embed/dashboard/"
            + self.get_token(payload)
            + "#bordered=true&titled=true"
        )
        return iframeUrl, params

    def post(self, request):
        iframes = []
        pprint(request.data)
        params = request.data.get("params", None)
        for dashboard_id in self.get_ids():
            iframe, params = self.create_iframe_url(dashboard_id, params)
            iframes.append({"iframe": iframe, "params": params})

        return JsonResponse({"iframes": iframes}, safe=True)
