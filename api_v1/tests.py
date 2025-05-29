import pytest
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from .views import TaskListCreateView, TaskDetailUpdateDeleteView
from to_do_app.models import Task


@pytest.fixture
def factory():
    return APIRequestFactory()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def task():
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        completed=False
    )

@pytest.fixture
def multiple_tasks():
    return [
        Task.objects.create(title=f'Task {i}', description=f'Description {i}', completed=False)
        for i in range(1, 4)
    ]


@pytest.mark.django_db
class TestTaskListCreateView:
    def test_create_task(self, factory, user):
        """Test POST request to create a task with forced authentication"""
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'completed': False
        }
        request = factory.post('/tasks/', data, format='json')
        force_authenticate(request, user=user)

        view = TaskListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Task'
        assert Task.objects.filter(title='New Task').exists()

    def test_create_task_invalid_data(self, factory, user):
        """Test POST request with invalid data"""
        data = {'description': 'Missing title'}
        request = factory.post('/tasks/', data, format='json')
        force_authenticate(request, user=user)

        view = TaskListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_tasks_list(self, factory, user, multiple_tasks):
        """Test GET request to get a task list with forced authentication"""
        request = factory.get('/tasks/')
        force_authenticate(request, user=user)

        view = TaskListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        assert response.data['results'][2]['title'] == 'Task 1'

    def test_filter_completed_tasks(self, factory, user, multiple_tasks):
        """Test filtering completed tasks"""
        task = multiple_tasks[0]
        task.completed = True
        task.save()

        request = factory.get('/tasks/', {'completed': 'true'})
        force_authenticate(request, user=user)

        view = TaskListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['completed'] is True

    def test_filter_by_title(self, factory, user, multiple_tasks):
        """Test filtering tasks by title (assuming your filter supports this)"""
        request = factory.get('/tasks/', {'title': 'Task 1'})
        force_authenticate(request, user=user)

        view = TaskListCreateView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK

        for task_data in response.data['results']:
            assert 'Task 1' in task_data['title']


@pytest.mark.django_db
class TestTaskDetailView:
    def test_get_task_detail_with_authentication(self, factory, user, task):
        """Test GET request to task detail with forced authentication"""
        request = factory.get(f'/tasks/{task.pk}/')
        force_authenticate(request, user=user)

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == task.title
        assert response.data['id'] == task.id

    def test_get_task_detail_without_authentication(self, factory, task):
        """Test GET request to task detail without authentication"""
        request = factory.get(f'/tasks/{task.pk}/')

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_task_detail_not_found(self, factory, user):
        """Test GET request for non-existent task"""
        request = factory.get('/tasks/999/')
        force_authenticate(request, user=user)

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=999)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_with_authentication(self, factory, user, task):
        """Test PUT request to update a task with forced authentication"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'completed': True
        }
        request = factory.put(f'/tasks/{task.pk}/', data, format='json')
        force_authenticate(request, user=user)

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Task'
        assert response.data['completed'] is True

        # Verify database was updated
        task.refresh_from_db()
        assert task.title == 'Updated Task'
        assert task.completed is True

    def test_partial_update_task_with_authentication(self, factory, user, task):
        """Test PATCH request to partially update a task"""
        data = {'completed': True}
        request = factory.patch(f'/tasks/{task.pk}/', data, format='json')
        force_authenticate(request, user=user)

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['completed'] is True

        task.refresh_from_db()
        assert task.completed is True
        assert task.title == 'Test Task'  # Should remain unchanged

    def test_update_task_without_authentication(self, factory, task):
        """Test PUT request without authentication"""
        data = {'title': 'Updated Task'}
        request = factory.put(f'/tasks/{task.pk}/', data, format='json')

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Verify task was not updated
        task.refresh_from_db()
        assert task.title == 'Test Task'

    def test_delete_task_with_authentication(self, factory, user, task):
        """Test DELETE request to delete a task"""
        task_id = task.id
        request = factory.delete(f'/tasks/{task.pk}/')
        force_authenticate(request, user=user)

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task_id).exists()

    def test_delete_task_without_authentication(self, factory, task):
        """Test DELETE request without authentication"""
        task_id = task.id
        request = factory.delete(f'/tasks/{task.pk}/')

        view = TaskDetailUpdateDeleteView.as_view()
        response = view(request, pk=task.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Task.objects.filter(id=task_id).exists()
