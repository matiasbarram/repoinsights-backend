from django.db.models import Max, F
from ...models import Project, Commit
from users.models import UserRepoInsightProject

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

    @staticmethod    
    def get_project_by_id(id):
        project = (
            Project.objects.using("repoinsights")
            .filter(id=id)
            .annotate(
                last_extraction_date=Max("extractions__date"),
                owner_name=F("owner__login")
            )
            .values("id", "name", "owner_name", "last_extraction_date", "language", "created_at")
            .distinct()
        )
        return project



    @staticmethod
    def user_selected(result: list, user_project_ids):
        for project in result:
            if project["id"] in user_project_ids:
                project["selected"] = True
            else:
                project["selected"] = False
        return result
