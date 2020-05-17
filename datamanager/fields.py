
from rest_framework import serializers
from datamanager.models import Task, Project
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class ModelObjectidField(serializers.Field):
    """
        We use this when we are doing bulk create/update. Since multiple instances share
        many of the same fk objects we validate and query the objects first, then modify the request data
        with the fk objects. This allows us to pass the objects in to be validated.
    """

    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        return data


class CurrentProjectDefault(object):
    requires_context = True

    def __call__(self, serializer_field):
        try:
            self.project = Project.objects.get(
                id=serializer_field.context["request"].parser_context["kwargs"][
                    "project_id"
                ]
            )
        except ObjectDoesNotExist:
            raise ValidationError("Project does not exist.")

        return self.project
