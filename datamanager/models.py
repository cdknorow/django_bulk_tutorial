from django.db import models
from django.db.models import signals
from django.utils import timezone


def update_project_last_modified(sender, instance, **kwargs):
    instance.project.last_modified = timezone.now()
    instance.project.save()


class Project(models.Model):
    name = models.CharField(max_length=200)
    last_modified = models.DateTimeField(auto_now=True)


class Task(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=200)
    last_modified = models.DateTimeField(auto_now=True)


signals.post_save.connect(update_project_last_modified, sender=Task)
signals.post_delete.connect(update_project_last_modified, sender=Task)
