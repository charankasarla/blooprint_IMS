from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

class UserAuthTests(APITestCase):
    
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'shiva',
            'password': 'shiva'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        # First, create a user
        self.test_user = User.objects.create_user(username='testuser', password='password123')
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class ItemTests(APITestCase):

    def setUp(self):
        # Create a user and get a token for authentication
        self.user = User.objects.create_user(username='testuser', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_item(self):
        url = reverse('item-create')  # Ensure this matches your path
        data = {
            'name': 'Laptop',
            'description': 'A brand new laptop'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Laptop')

    def test_get_item(self):
        # Create an item to get
        item = Item.objects.create(name='Laptop', description='A brand new laptop')
        url = reverse('item-detail', kwargs={'item_id': item.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_update_item(self):
        # Create an item to update
        item = Item.objects.create(name='Laptop', description='A brand new laptop')
        url = reverse('item-detail', kwargs={'item_id': item.id})
        data = {
            'name': 'Updated Laptop',
            'description': 'An updated description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=item.id).name, 'Updated Laptop')

    def test_delete_item(self):
        # Create an item to delete
        item = Item.objects.create(name='Laptop', description='A brand new laptop')
        url = reverse('item-detail', kwargs={'item_id': item.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

class ItemCachingTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.item = Item.objects.create(name='Laptop', description='A brand new laptop')

    def test_item_caching(self):
        url = reverse('item-detail', kwargs={'item_id': self.item.id})

        # First request (should not be cached)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

        # Store the response in cache
        cache.set(f'item_{self.item.id}', response.data, timeout=60)

        # Second request (should be served from cache)
        cached_response = cache.get(f'item_{self.item.id}')
        self.assertIsNotNone(cached_response)
        self.assertEqual(cached_response['name'], 'Laptop')
class ItemAuthTests(APITestCase):

    def test_access_without_token(self):
        url = reverse('item-create')
        data = {
            'name': 'Laptop',
            'description': 'A brand new laptop'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_token(self):
        user = User.objects.create_user(username='testuser', password='password123')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('item-create')
        data = {
            'name': 'Laptop',
            'description': 'A brand new laptop'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
