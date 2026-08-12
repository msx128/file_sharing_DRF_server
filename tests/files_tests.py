from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from files.models import File
import pytest

@pytest.mark.django_db
class TestFiles:
    def test_authenticated_create_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201
        assert File.objects.filter(user=user).exists()

    def test_unauthenticated_create_file(self, api_client):
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 401
        assert not File.objects.all().exists()

    def test_authenticated_invalid_create_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        response = api_client.post(
            reverse('files'),
            {'file': 'hi'},
        )
        assert response.status_code == 400
        assert not File.objects.filter(user=user).exists()

    def test_get_files(self, api_client):
        responce = api_client.get(
            reverse('files'),
        )
        assert responce.status_code == 200

    def test_authenticated_delete_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201

        file_obj = File.objects.get(user=user)

        response = api_client.delete(
            reverse('file_details', args=[file_obj.id])
        )
        assert response.status_code == 204
        assert not File.objects.filter(user=user).exists()

    def test_other_authenticated_delete_file(self, api_client, user, userB):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201

        file_obj = File.objects.get(user=user)

        api_client.force_authenticate(user=userB)

        response = api_client.delete(
            reverse('file_details', args=[file_obj.id])
        )
        assert response.status_code == 403
        assert File.objects.all().exists()
        
    def test_unauthenticated_delete_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201

        file_obj = File.objects.get(user=user)

        api_client.force_authenticate(user=None)

        response = api_client.delete(
            reverse('file_details', args=[file_obj.id])
        )
        assert response.status_code == 401
        assert File.objects.all().exists()

    def test_title_extention_extration(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201
        assert response.data['title'] == 'test'
        assert response.data['extention'] == 'txt'

    def test_other_user_get(self, api_client, user, userB):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201

        file_obj = File.objects.get(user=user)

        api_client.force_authenticate(user=userB)

        response = api_client.get(
            reverse('file_details', args=[file_obj.id])
        )
        assert response.status_code == 200

    
    def test_db_behavior_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )

        response = api_client.post(
            reverse('files'),
            {'file': uploaded_file},
        )
        assert response.status_code == 201
        assert File.objects.filter(user=user).count() == 1

        other_uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )
        # for some reason it needs separate variable otherwise bad_request
        # maybe it something about object relationships, like if remembers exact object id
        response = api_client.post(
            reverse('files'),
            {'file': other_uploaded_file}, 
        )
        assert response.status_code == 201
        assert File.objects.filter(user=user).count() == 2
