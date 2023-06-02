from pprint import pprint

from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Project
from django.db.models import F


class RepoInsightsProjects(APIView):
    def get(self, request):
        projects = list(
            Project.objects.using("repoinsights")
            .values("id", "name", owner_name=F("owner__login"))
            .filter(forked_from__isnull=True, deleted=False, private=False)
        )
        languages = list(
            Project.objects.using("repoinsights")
            .filter(forked_from__isnull=True, deleted=False)
            .values_list("language", flat=True)
            .distinct()
        )

        response = {
            "projects": {"data": projects, "total": len(projects)},
            "languages": {"data": languages, "total": len(languages)},
        }
        return JsonResponse(response, safe=True)
