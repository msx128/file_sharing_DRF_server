import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='alice', password='123')

@pytest.fixture
def userB():
    return User.objects.create_user(username='anna', password='123')
