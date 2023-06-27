from pprint import pprint

from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Project
from django.db.models import F, Count, Max

from users.models import UserRepoInsightProject


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


class RepoInsightsProjectsFilters(APIView):
    def get(self, request):
        if "langs" in request.GET.get("filter"):
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
        
        if "user" in request.GET.get("filter"):
            current_user_id = request.user.id
            user_project_ids = list(UserRepoInsightProject.objects.filter(user_id=current_user_id).values_list(
                "repoinsight_project_id", flat=True
            ))

            response = {"data": [{
                "name": "Mis proyectos",
                "count": len(user_project_ids)
            }]
            }

            return JsonResponse(response, safe=True)
            
            # projects = (
            #     Project.objects.using("repoinsights")
            #     .filter(id__in=user_project_ids)
            #     .values("id", "name", owner_name=F("owner__login"))
            #     .filter(forked_from__isnull=True, deleted=False, private=False)
            # )
    

class RepoInsightsExplore(APIView):

    def get_user_project_ids(self, current_user_id: int):
        return UserRepoInsightProject.objects.filter(user_id=current_user_id).values_list(
                    "repoinsight_project_id", flat=True
                )


    def user_selected(self, result: list, user_project_ids):
        for project in result:
            if project["id"] in user_project_ids:
                project["selected"] = True
            else:
                project["selected"] = False
        return result


    def get(self, request):
        langs = request.GET.get("langs")
        commits = request.GET.get("commits")
        stars = request.GET.get("stars")
        current_user_id = request.user.id
        user = request.GET.get("user")


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

        if user:
            user_project_ids = list(self.get_user_project_ids(current_user_id))
            projects = projects.filter(id__in=user_project_ids)

        if langs:
            langs = langs.split(",")
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
        user_project_ids = self.get_user_project_ids(current_user_id)

        self.user_selected(result, user_project_ids)


        response = {"data": result, "total": total}
        return JsonResponse(response, safe=True)
