from django.db.models import Count, F, Max, Subquery, OuterRef
from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import Project, Commit

from .helper.variables import LANGS, COMMIT, USER, SORT
from .helper.filter_data_manager import FilterDataManager
from .helper.project_manager import ProjectManager
from .helper.metric_score import ProjectMetricScore


class RepoInsightsExplore(APIView):
    @staticmethod
    def project_filtered_by_commits(projects, min_total: int, max_total: int):
        commit_count = (
            Commit.objects.using("repoinsights")
            .filter(project_id=OuterRef("id"))
            .values("project_id")
            .annotate(total=Count("id"))
            .values("total")
        )
        return projects.annotate(commit_count=Subquery(commit_count)).filter(
            commit_count__gte=min_total, commit_count__lte=max_total
        )

    def get(self, request):
        current_user_id = request.user.id
        sort = int(request.GET.get(SORT)) if request.GET.get(SORT) else None
        langs = request.GET.get(LANGS)
        commits = request.GET.get(COMMIT)
        user = request.GET.get(USER)

        projects = ProjectManager.get_projects()
        if user:
            user_project_ids = list(
                ProjectManager.get_user_project_ids(current_user_id)
            )
            projects = projects.filter(id__in=user_project_ids)

        if langs:
            langs = langs.split(",")
            projects = projects.filter(language__in=langs)

        if commits:
            commits_list: list = commits.split(",")
            for commit in commits_list:
                min_limit, max_limit = FilterDataManager.get_intervals(commit)
                projects = self.project_filtered_by_commits(
                    projects, min_limit, max_limit
                )

        result = ProjectMetricScore.calc_metric_score(projects)
        total = len(result)
        user_project_ids = ProjectManager.get_user_project_ids(current_user_id)
        result = ProjectManager.user_selected(result, user_project_ids)
        result = FilterDataManager.sort_by(result, sort) if sort else result

        response = {"data": result, "total": total}
        return JsonResponse(response, safe=True)


class RepoInsightsExploreProject(APIView):
    def get(self, request, project_id):
        projects = ProjectManager.get_project_by_id(project_id)
        projects = ProjectMetricScore.calc_metric_score(projects)
        user_projects = ProjectManager.get_user_project_ids(request.user.id)
        project = list(projects)[0]
        project["selected"] = True if project_id in user_projects else False
        return JsonResponse(project, safe=False)
