from django.shortcuts import render
from rest_framework import generics
from datamanager.serializers import TaskSerializer, BulkTaskSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from datamanager.models import Task, Project
from rest_framework.urls import url

# Create your views here.


def validate_ids(data, field="id", unique=True):

    if isinstance(data, list):
        id_list = [int(x[field]) for x in data]

        if unique and len(id_list) != len(set(id_list)):
            raise ValidationError("Multiple updates to a single {} found".format(field))

        return id_list

    return [data]


class TaskUpdateView(generics.UpdateAPIView):
    """
    # Update the Taks
    """

    lookup_field = "id"
    serializer_class = TaskSerializer

    def get_queryset(self):

        return Task.objects.filter(
            project__id=self.kwargs["project_id"], id=self.kwargs["id"],
        )


class TaskListCreatetUpdateView(generics.ListCreateAPIView):
    """
    # List/Create/Update the relationships between Labels and CaptureSamples

    Required permissions: *Authenticated*, *CaptureLabelValue add*
    """

    serializer_class = TaskSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(TaskListCreatetUpdateView, self).get_serializer(*args, **kwargs)

    def get_queryset(self, ids=None):
        if ids:
            return Task.objects.filter(
                project__id=self.kwargs["project_id"], id__in=ids,
            )

        return Task.objects.filter(project__id=self.kwargs["project_id"])

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        ids = validate_ids(request.data)

        instances = self.get_queryset(ids=ids)

        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class TaskBulkListCreatetUpdateView(generics.ListCreateAPIView):
    """
    # List/Create/Update the relationships between Labels and CaptureSamples

    Required permissions: *Authenticated*, *CaptureLabelValue add*
    """

    serializer_class = BulkTaskSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(TaskBulkListCreatetUpdateView, self).get_serializer(
            *args, **kwargs
        )

    def get_queryset(self, ids=None):
        if ids:
            return Task.objects.filter(
                project__pk=self.kwargs["project_id"], id__in=ids,
            )

        return Task.objects.filter(project__id=self.kwargs["project_id"],)

    def post(self, request, *args, **kwargs):

        project = Project.objects.get(id=kwargs["project_id"])

        if isinstance(request.data, list):
            for item in request.data:
                item["project"] = project
        else:
            raise ValidationError("Invalid Input")

        return super(TaskBulkListCreatetUpdateView, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        project = Project.objects.get(id=kwargs["project_id"])

        ids = validate_ids(request.data)

        if isinstance(request.data, list):
            for item in request.data:
                item["project"] = project
        else:
            raise ValidationError("Invalid Input")

        instances = self.get_queryset(ids=ids)

        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        data = serializer.data
        return Response(data)

    def perform_update(self, serializer):
        serializer.save()
