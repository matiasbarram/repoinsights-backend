from pprint import pprint

from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Project
from django.db.models import F, Count, Max

from users.models import UserRepoinsihtProject


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


class RepoInsightsProjectsLangs(APIView):
    def get(self, request):
        langs_with_counts = (
            Project.objects.using("repoinsights")
            .filter(forked_from__isnull=True, deleted=False, private=False, language__isnull=False)
            .values("language")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        
        langs = [{"name": lang["language"], "count": lang["total"]} for lang in langs_with_counts]
        
        response = {"data": langs, "total": len(langs)}
        return JsonResponse(response, safe=True)
    

class RepoInsightsExplore(APIView):

    def get(self, request):
        langs = request.GET.get("langs")
        commits = request.GET.get("commits")
        stars = request.GET.get("stars")
        current_user_id = request.user.id


        projects = (
            Project.objects.using("repoinsights")
            .filter(forked_from__isnull=True, deleted=False, private=False)
            .annotate(
                last_extraction_date=Max("extractions__date"),
                owner_name=F("owner__login")
            )
            .values("id", "name", "owner_name", "last_extraction_date", "language", "created_at")
            .distinct()
        )

        if langs:
            langs = langs.split(",")  # Separar los lenguajes en una lista
            projects = projects.filter(language__in=langs)

        # if commits:
        #     # Aplicar filtro de commits
        #     # Aquí debes implementar la lógica para filtrar por el rango de commits
        #     projects = projects.filter(...)

        # if stars:
        #     # Aplicar filtro de estrellas
        #     # Aquí debes implementar la lógica para filtrar por el rango de estrellas
        #     projects = projects.filter(...)

        result = list(projects)
        total = len(result)

        user_project_ids = UserRepoinsihtProject.objects.filter(user_id=current_user_id).values_list(
            "repoinsight_project_id", flat=True
        )

        for project in result:
            if project["id"] in user_project_ids:
                project["selected"] = True
            else:
                project["selected"] = False

        response = {"data": result, "total": total}
        return JsonResponse(response, safe=True)
