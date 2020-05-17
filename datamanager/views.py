from django.shortcuts import render
from rest_framework import generics
from datamanager.serializers import TaskSerializer, BulkTaskSerializer
import uuid
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from datamanager.models import Task, Project
from rest_framework.urls import url

# Create your views here.


def validate_uuids(data, field="uuid", unique=True):

    if isinstance(data, list):
        uuid_list = [uuid.UUID(x[field]) for x in data]

        if unique and len(uuid_list) != len(set(uuid_list)):
            raise ValidationError("Multiple updates to a single {} found".format(field))

        return uuid_list

    return [uuid.UUID(data)]


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

    def get_queryset(self, uuids=None):
        if uuids:
            return Task.objects.filter(
                project__uuid=self.kwargs["project_uuid"], uuid__in=uuids,
            )

        return Task.objects.filter(project__uuid=self.kwargs["project_uuid"])

    def post(self, request, *args, **kwargs):

        return super(TaskListCreatetUpdateView, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        uuids = validate_uuids(request.data)
        instances = self.get_queryset(uuids=uuids)
        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)


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

    def get_queryset(self, uuids=None):
        if uuids:
            return Task.objects.filter(
                project__uuid=self.kwargs["project_uuid"], uuid__in=uuids,
            )

        return Task.objects.filter(project__uuid=self.kwargs["project_uuid"],)

    def post(self, request, *args, **kwargs):

        project = Project.objects.get(uuid=kwargs["project_uuid"])

        if isinstance(request.data, list):
            for item in request.data:
                item["project"] = project
        else:
            raise ValidationError("Invalid Input")

        return super(TaskBulkListCreatetUpdateView, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        uuids = validate_uuids(request.data)
        instances = self.get_queryset(uuids=uuids)
        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
