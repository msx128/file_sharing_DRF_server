import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from files.models import File


def response_on_get(api_client):
    return api_client.get(reverse('files'))

def response_on_post(api_client, uploaded_file):
    return api_client.post(reverse('files'), {'file': uploaded_file})

def response_on_delete(api_client, id): 
    return api_client.delete(reverse('file_details', args=[id]))
  

@pytest.mark.django_db
class TestFiles:
    def test_authenticated_create_file(self, api_client, user, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        assert File.objects.filter(user=user).exists()

    def test_unauthenticated_create_file(self, api_client, uploaded_file):
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 401
        assert not File.objects.all().exists()

    def test_authenticated_invalid_create_file(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse('files'), {'file': 'hi'},)
        assert response.status_code == 400
        assert not File.objects.filter(user=user).exists()

    def test_get_files(self, api_client):
        response = response_on_get(api_client)
        assert response.status_code == 200

    def test_authenticated_delete_file(self, api_client, user, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client,uploaded_file)
        assert response.status_code == 201
        file_obj = File.objects.get(user=user)
        response = response_on_delete(api_client, file_obj.id)
        assert response.status_code == 204
        assert not File.objects.filter(user=user).exists()

    def test_other_authenticated_delete_file(self, api_client, user, userB, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        file_obj = File.objects.get(user=user)
        api_client.force_authenticate(user=userB)
        response = response_on_delete(api_client, file_obj.id)
        assert response.status_code == 403
        assert File.objects.all().exists()
        
    def test_unauthenticated_delete_file(self, api_client, user, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        file_obj = File.objects.get(user=user)
        api_client.force_authenticate(user=None)
        response = response_on_delete(api_client, file_obj.id)
        assert response.status_code == 401
        assert File.objects.all().exists()

    def test_title_extention_extration(self, api_client, user, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        assert response.data['title'] == 'test'
        assert response.data['extention'] == 'txt'
        # if make this more robust I should return uploaded file as
        # a unit with name, obj, ext, and maybe separatly uploaded_file
        # like (uploaded_file, (obj,name,ext))
        # but isn't it to complex?

    def test_other_user_get(self, api_client, user, userB, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        api_client.force_authenticate(user=userB)
        response_on_get(api_client)
        assert response.status_code == 200

    
    def test_db_behavior_file(self, api_client, user, uploaded_file):
        api_client.force_authenticate(user=user)
        response = response_on_post(api_client, uploaded_file)
        assert response.status_code == 201
        assert File.objects.filter(user=user).count() == 1
        other_uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'hello, world!',
            content_type='text/plain',
        )
        # for some reason it needs separate variable otherwise bad_request
        # maybe it something about object relationships, like if remembers exact object id
        # need to rethink how exact same objects behave
        # I think that they anyway should be "different"
        # like when you apload the same file as other completely separate
        # person, you don't want to be "dependend" on their file
        # throught I can just create user list and it would be like
        # Arc in rust, or smart_ptr in C++(don't know how they works, but I bet something similar) 
        # but why this error so
        response = response_on_post(api_client, other_uploaded_file)
        assert response.status_code == 201
        assert File.objects.filter(user=user).count() == 2
