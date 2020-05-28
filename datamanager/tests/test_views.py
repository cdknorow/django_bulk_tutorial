
from datamanager.models import Project, Task
from rest_framework import status
from rest_framework.reverse import reverse
import json
import pytest

# Create your tests here.

pytestmark = pytest.mark.django_db  # All tests use db


TEST_SIZE = 100

@pytest.fixture
def project():
    return Project.objects.create(name='Test')



@pytest.fixture
def tasks(project):
    tasks = []
    for i in range(TEST_SIZE):
        tasks.append(Task.objects.create(project=project, name='Test_{}'.format(i)))

    return tasks


class TestTaskUpdate():
    def test_update_task(self,client, project, tasks):

        for x in range(TEST_SIZE):
            test_url = reverse(
                "project-task-update",
                kwargs={
                    "project_id": project.id,
                    "id": tasks[x].id
                },
            )
            # test auto setting sequence
            response = client.put(
                test_url,
                data = {'name':'Test_{0}_{0}'.format(x),
                        'description':"test",
                       }
            )

            assert response.status_code == status.HTTP_200_OK

    def test_update_list_serializer(self,client, project, tasks):
        test_url = reverse(
            "project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )
        data = [{"name": "Test_{0}_{0}".format(x.id), "description": "Test", 'id':x.id} for x in tasks]

        response = client.put(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == TEST_SIZE


    def test_bulk_update(self, client, project, tasks):
        test_url = reverse(
            "v2-project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )

        data = [{"name": "Test_{0}_{0}".format(x.id), "description": "Test", 'id':x.id} for x in tasks]

        response = client.put(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == TEST_SIZE





class TestTaskCreate():
    def test_create_task(self,client, project):
        test_url = reverse(
            "project-task-list-create-update",
            kwargs={
                "project_id": project.id,
            },
        )

        for x in range(TEST_SIZE):
            # test auto setting sequence
            response = client.post(
                test_url,
                data = {'name':'Test_{}'.format(x), 'description':"test"}
            )
            assert response.status_code == status.HTTP_201_CREATED

    def test_list_serializer(self,client, project):
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


