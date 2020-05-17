from rest_framework import serializers
from django.db import IntegrityError
from datamanager.models import Task, Project
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from datamanager.fields import ModelObjectidField, CurrentProjectDefault


class CreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return [self.child.create(attrs) for attrs in validated_data]

    def update(self, instances, validated_data):

        # speed optimization
        instances_hash = {instance.id: instance for instance in instances}

        result = [
            self.child.update(instances_hash.get(attrs["id"]), attrs)
            for attrs in validated_data
        ]

        return result


class BulkCreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        update_project_last_modified(result)

        return result

    def update(self, instances, validated_data):

        # speed optimization
        instances_hash = {instances.id: instance for instance in instances}

        result = [
            self.child.update(instances_hash.get(attrs["id"]), attrs)
            for attrs in validated_data
        ]

        writable_fields = [
            x
            for x in self.child.Meta.fields
            if x not in self.child.Meta.read_only_fields
        ]

        # bulk update doesn't modify auto_now fields in django
        if "last_modified" in self.child.Meta.fields:
            writable_fields += ["last_modified"]
            last_modified = timezone.now()
            for instance in result:
                instance.last_modified = last_modified

        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        update_project_last_modified(result)

        return result


def update_project_last_modified(instances):

    if isinstance(instances, list):
        project = instances[0].project
        project.last_modified = timezone.now()
        project.save()


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.HiddenField(default=CurrentProjectDefault())

    def create(self, validated_data):

        instance = Task(**validated_data)

        instance.save()

        return instance

    def update(self, instance, validated_data):

        instance.description = validated_data["description"]
        instance.name = validated_data["name"]

        instance.save()

        return instance

    class Meta:
        model = Task
        fields = ("id", "name", "project", "description", "last_modified")
        read_only_fields = ("id", "last_modiied")
        list_serializer_class = CreateUpdateListSerializer


class BulkTaskSerializer(serializers.ModelSerializer):
    project = ModelObjectidField()

    def create(self, validated_data):
        instance = Task(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    def update(self, instance, validated_data):

        instance.description = validated_data["description"]
        instance.name = validated_data["name"]

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = Task
        fields = ("id", "name", "project", "description", "last_modified")
        read_only_fields = ("id", "last_modiied")
        list_serializer_class = BulkCreateUpdateListSerializer
