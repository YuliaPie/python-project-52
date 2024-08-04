import pytest
from django.test import Client
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status


@pytest.fixture
def user(db):
    CustomUserModel = get_user_model()
    user = CustomUserModel.objects.create_user(username='testuser', password='testpass')
    return user


@pytest.fixture
def another_user(db):
    model = get_user_model()
    user = model.objects.create_user(username='anotheruser', password='anotherpass')
    return user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture(params=[{'name': 'testname', 'surname': 'testsurname', 'username': 'testuser',
                         'password': 'testpassword', 'password2': 'testpassword'}])
def form_data(request):
    return request.param


@pytest.fixture(params=[{'name': 'ok', 'surname': 'ok', 'username': '*bad',
                         'password': '1', 'password2': '2'}])
def invalid_form_data(request):
    return request.param


@pytest.fixture(params=[{'name': 'ok'}])
def status_form_data(request):
    return request.param


@pytest.fixture
def status(db):
    status = Status.objects.create_status(name='test')
    return status