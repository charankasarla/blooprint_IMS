from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Item

class ItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_item(self):
        response = self.client.post(reverse('create_item'), {'name': 'Item1', 'description': 'Test item'})
        self.assertEqual(response.status_code, 201)

    def test_read_item(self):
        item = Item.objects.create(name='Item2', description='Another item')
        response = self.client.get(reverse('read_item', args=[item.id]))
        self.assertEqual(response.status_code, 200)
