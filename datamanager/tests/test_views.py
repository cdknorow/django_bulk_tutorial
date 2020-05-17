
from datamanager.models import Project, Task
from rest_framework import status
from rest_framework.reverse import reverse
import json
import pytest

# Create your tests here.

pytestmark = pytest.mark.django_db  # All tests use db


TEST_SIZE = 10000

@pytest.fixture
def project():
    return Project.objects.create(name='Test')


class TestTask():
    def test_create_task(self,client, project):
        test_url = reverse(
            "project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )

        # test auto setting sequence
        response = client.post(
            test_url,
            data = {'name':'Test', 'description':"test"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_bulk_create(self,client, project):
        test_url = reverse(
            "project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )
        data = [{"name": "MyTask_{}".format(x), "description": "Test"} for x in range(TEST_SIZE)]

        response = client.post(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert len(response.json()) == TEST_SIZE


class TestBulkTask():

    def test_bulk_create(self, client, project):
        test_url = reverse(
            "v2-project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )
        data = [{"name": "MyTask_{}".format(x), "description": "Test"} for x in range(TEST_SIZE)]

        response = client.post(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert len(response.json()) == TEST_SIZE


