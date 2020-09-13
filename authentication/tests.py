from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from freezegun import freeze_time
from rest_framework.test import APITestCase, APIRequestFactory

from . import views


class TestLogin(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('testusername', password='testpassword')

    def test_http_200_and_token_returned_if_correct_credentials(self):
        request = self.factory.post(
            reverse('login'),
            {
                'username': 'testusername',
                'password': 'testpassword',
            },
            format='json'
        )
        response = views.login(request)
        assert response.status_code == 200
        assert 'token' in response.data

    def test_http_400_if_incorrect_credentials(self):
        request = self.factory.post(
            reverse('login'),
            {
                'username': 'testusername',
                'password': 'wrongpassword',
            },
            format='json'
        )
        response = views.login(request)
        assert response.status_code == 400

    def test_http_400_if_no_credentials(self):
        request = self.factory.post(
            reverse('login'),
            {},
            format='json'
        )
        response = views.login(request)
        assert response.status_code == 400


class TestProtected(APITestCase):

    @property
    def valid_token(self):
        request = self.factory.post(
            reverse('login'),
            {
                'username': 'testusername',
                'password': 'testpassword',
            },
            format='json'
        )
        response = views.login(request)
        return response.data.get('token')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('testusername', password='testpassword')

    def test_http_200_if_valid_token(self):
        request = self.factory.get(
            reverse('protected'),
            HTTP_AUTHORIZATION=self.valid_token,
        )
        response = views.protected(request)
        assert response.status_code == 200

    def test_http_403_if_invalid_token(self):
        request = self.factory.get(
            reverse('protected'),
            HTTP_AUTHORIZATION='invalidtoken',
        )
        response = views.protected(request)
        assert response.status_code == 403

    def test_http_403_if_no_token(self):
        request = self.factory.get(
            reverse('protected'),
        )
        response = views.protected(request)
        assert response.status_code == 403

    def test_http_403_if_expired_token(self):
        request = self.factory.get(
            reverse('protected'),
            HTTP_AUTHORIZATION=self.valid_token,
        )
        with freeze_time(timezone.now() + timezone.timedelta(seconds=61)):
            response = views.protected(request)
        assert response.status_code == 403
