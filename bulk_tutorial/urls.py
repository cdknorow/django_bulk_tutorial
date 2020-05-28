"""bulk_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from datamanager.views import (
    TaskListCreatetUpdateView,
    TaskBulkListCreatetUpdateView,
    TaskUpdateView,
)
from rest_framework.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    url(
        r"^project/(?P<project_id>[^/]+)/task/$",
        TaskListCreatetUpdateView.as_view(),
        name="project-task-list-create-update",
    ),
    url(
        r"^v2/project/(?P<project_id>[^/]+)/task/$",
        TaskBulkListCreatetUpdateView.as_view(),
        name="v2-project-task-list-create-update",
    ),
    url(
        r"^project/(?P<project_id>[^/]+)/task/(?P<id>[^/]+)$",
        TaskUpdateView.as_view(),
        name="project-task-update",
    ),
]
