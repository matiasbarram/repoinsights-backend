from django.db.models import F
from django.http import JsonResponse
from rest_framework.views import APIView

from .helper.project_manager import ProjectManager

class RepoInsightsProjects(APIView):
    def get(self, request):
        user_id = request.user.id
        projects = list(ProjectManager.get_projects())
        languages = list(ProjectManager.get_languages())
        user_projects = list(ProjectManager.get_user_project_ids(user_id))
        projects = ProjectManager.user_selected(projects, user_projects)

        response = {
            "projects": {"data": projects, "total": len(projects)},
            "languages": {"data": languages, "total": len(languages)},
        }
        return JsonResponse(response, safe=True)
