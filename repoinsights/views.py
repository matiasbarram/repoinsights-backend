import json
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Count, F, Max, Subquery, OuterRef
from django.db import connections

from users.models import UserRepoInsightProject
from repoinsights.models import Project, Commit


COMMIT = "commit"
LANGS = "langs"
USER = "user"


class ProjectManager:
    @staticmethod
    def get_user_project_ids(current_user_id: int):
        return UserRepoInsightProject.objects.filter(user_id=current_user_id).values_list(
            "repoinsight_project_id", flat=True
        )

    @staticmethod
    def get_user_projects(current_user_id: int):
        user_project_ids = list(ProjectManager.get_user_project_ids(current_user_id))
        projects = (
            Project.objects.using("repoinsights")
            .filter(forked_from__isnull=True, deleted=False, private=False)
            .values("id", "name", "language", "selected")
            .filter(id__in=user_project_ids)
        )
        return projects

    @staticmethod
    def get_projects():
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
        return projects


class FilterDataManager:
    @staticmethod
    def get_languages(projects):
        langs = projects.values_list("language", flat=True).distinct()
        lang_count = []
        for lang in langs:
            lang_count.append({"name": lang, "total": projects.filter(language=lang).count(), "language": lang})
        return lang_count
    

    @staticmethod
    def get_intervals(commit):
        return commit.split(" - ")
                        

    @staticmethod
    def get_projects_by_commits(projects, min, max):
        commit_count = Commit.objects.using("repoinsights").filter(
            project_id=OuterRef("id")
        ).values("project_id").annotate(total=Count("id")).values("total")
        projects = projects.annotate(commit_count=Subquery(commit_count)).filter(
            commit_count__gte=min, commit_count__lte=max
        )
        return projects

    @staticmethod
    def get_commits_data(user_project_ids, langs):
        project_condition = f"AND p.id IN ({','.join([str(project_id) for project_id in user_project_ids])})" if user_project_ids else ""
        lang_condition = "AND p.language IN ({})".format(','.join(["'{}'".format(lang) for lang in langs])) if langs else ""

        query = f"""
            SELECT 
                CASE
                    WHEN total >= 100000 THEN '100000 - more'
                    WHEN total < 1000 THEN '0 - 1000'
                    ELSE CONCAT((FLOOR(total / 5000) * 5000), ' - ', ((FLOOR(total / 5000) + 1) * 5000))
                END AS total_interval,
                COUNT(*) AS project_count
            FROM
                (
                    SELECT 
                        CONCAT(u.login, '/', p.name) AS project_owner,
                        COUNT(c.project_id) AS total
                    FROM 
                        commits c 
                    JOIN 
                        projects p ON p.id = c.project_id
                    JOIN 
                        users u ON u.id = p.owner_id
                    WHERE 
                        p.forked_from IS NULL
                        {project_condition}
                        {lang_condition}
                    GROUP BY  
                        project_owner
                ) AS subquery
            GROUP BY
                total_interval
            ORDER BY 
                MIN(total) DESC;
        """
        cursor = connections['repoinsights'].cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        data = []
        for result in results:
            name, count = result
            if name == "0 - 5000":
                name = "1000 - 5000"
            data.append({"name": name, "count": count})
        return data


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
        user_filter = request.GET.get(USER)
        langs_filter = request.GET.get(LANGS)
        commits_filter = request.GET.get(COMMIT)
        current_user_id: int = request.user.id
        response = {}

        filters = [LANGS, USER, COMMIT]
        filter_data ={
            LANGS: {
                "title": "Lenguajes",
                "key": LANGS,
            },
            USER: {
                "title": "Usuario",
                "key": USER,
            },
            COMMIT: {
                "title": "Commits",
                "key": COMMIT,
            },
        }

        if USER in filters:
            if current_user_id is None:
                JsonResponse({"error": "No user id found"}, status=500)

            user_project_ids = list(ProjectManager.get_user_project_ids(current_user_id))
            response[USER] = {
                "data": [{"name": "Mis proyectos", "count": len(user_project_ids)}],
                "info": filter_data[USER],
            }

        if LANGS in filters:
            if user_filter:
                user_project_ids = list(ProjectManager.get_user_project_ids(current_user_id))
                projects = ProjectManager.get_projects().filter(id__in=user_project_ids)
            else:
                projects = (
                    Project.objects.using("repoinsights")
                    .filter(forked_from__isnull=True, deleted=False, private=False, language__isnull=False)
                )
     
            commits = commits_filter.split(",") if commits_filter else None
            if commits:
                for commit in commits:
                    min_limit, max_limit = FilterDataManager.get_intervals(commit)
                    projects = FilterDataManager.get_projects_by_commits(projects, min_limit, max_limit)
            langs_with_counts = FilterDataManager.get_languages(projects)
            langs = [{"name": lang["language"], "count": lang["total"]} for lang in langs_with_counts]
            response[LANGS] = {"data": langs, 
                                 "total": len(langs),
                                 "info": filter_data[LANGS]
                                 }
        if COMMIT in filters:
            user_project_ids = list(ProjectManager.get_user_project_ids(current_user_id)) if user_filter else []
            langs = langs_filter.split(",") if langs_filter else []
            data = FilterDataManager.get_commits_data(user_project_ids, langs)
            
            response[COMMIT] = {"data": data,
                                    "total": len(data),
                                    "info": filter_data[COMMIT]
                                    }
        return JsonResponse(response, safe=True)


class RepoInsightsExplore(APIView):

    @staticmethod
    def project_filtered_by_commits(projects, min_total: int, max_total: int):
        commit_count = Commit.objects.using("repoinsights").filter(
            project_id=OuterRef("id")
        ).values("project_id").annotate(total=Count("id")).values("total")
        return projects.annotate(commit_count=Subquery(commit_count)).filter(
            commit_count__gte=min_total, commit_count__lte=max_total
        )

    @staticmethod
    def user_selected(result: list, user_project_ids):
        for project in result:
            if project["id"] in user_project_ids:
                project["selected"] = True
            else:
                project["selected"] = False
        return result

    def get(self, request):
        langs = request.GET.get(LANGS)
        commits = request.GET.get(COMMIT)
        stars = request.GET.get("stars")
        current_user_id = request.user.id
        user = request.GET.get(USER)

        projects = ProjectManager.get_projects()

        if user:
            user_project_ids = list(ProjectManager.get_user_project_ids(current_user_id))
            projects = projects.filter(id__in=user_project_ids)

        if langs:
            langs = langs.split(",")
            projects = projects.filter(language__in=langs)

        if commits:
            commits_list: list = commits.split(",")
            for commit in commits_list:
                min_limit, max_limit = FilterDataManager.get_intervals(commit)
                projects = self.project_filtered_by_commits(projects, min_limit, max_limit)

        result = list(projects)
        total = len(result)
        user_project_ids = ProjectManager.get_user_project_ids(current_user_id)

        self.user_selected(result, user_project_ids)

        response = {"data": result, "total": total}
        return JsonResponse(response, safe=True)
