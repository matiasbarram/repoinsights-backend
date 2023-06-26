from django.db import models


class User(models.Model):
    class Meta:
        db_table = "users"
        managed = False

    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    ext_ref_id = models.CharField(max_length=32, null=False)
    type = models.CharField(max_length=255, default="USR", null=False)


class Project(models.Model):
    class Meta:
        db_table = "projects"
        managed = False

    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    ext_ref_id = models.CharField(max_length=32, null=False)
    forked_from = models.IntegerField(null=True)
    deleted = models.BooleanField(default=False, null=False)
    private = models.BooleanField(null=False, default=False, blank=False)

class Extractions(models.Model):
    class Meta:
        db_table = "extractions"
        managed = False

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="extractions")
    date = models.DateTimeField()
    ext_ref_id = models.CharField(max_length=32)
