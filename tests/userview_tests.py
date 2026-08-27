import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUsers:
    def test_get_users(self, api_client):
        response = api_client.get(
            reverse('users'),
        )
        assert response.status_code == 200

    def test_get_user_details(self, api_client, user):
        response = api_client.get(reverse('user_details', args=[user.id]))
        assert response.status_code == 200
        

    # maybe add some more tests, but considering User is not my module
    # I can say that it reliable
    
