import boto3
import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='alice', password='123')

@pytest.fixture
def userB():
    return User.objects.create_user(username='anna', password='123')

@pytest.fixture()
def s3_client():
    return boto3.client('s3')

@pytest.fixture(autouse=True)
def check_s3_cleanup(s3_client):
    before = s3_client.list_objects(Bucket='allpurpose-bucket')
    yield
    after = s3_client.list_objects(Bucket='allpurpose-bucket')
    assert before == after, "Test left files in s3"

@pytest.fixture
def uploaded_file():
    return SimpleUploadedFile(
        'test.txt',
        b'Hello, World!',
        content_type='text/plain',
    )
