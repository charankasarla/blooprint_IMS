from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ItemList(APIView):
    def get(self, request):
        """
        Retrieve all items from the inventory, with caching.
        """
        cached_items = cache.get('all_items')
        
        if cached_items is not None:
            return Response(cached_items, status=status.HTTP_200_OK)
        
        items = Item.objects.all() 
        serializer = ItemSerializer(items, many=True)
        
        cache.set('all_items', serializer.data, timeout=60*15)

        return Response(serializer.data, status=status.HTTP_200_OK)
class ItemGet(APIView):
    def get(self, request, item_id):
        cache_key = f'item_{item_id}'
        item = cache.get(cache_key)

        if not item:
            try:
                item = Item.objects.get(id=item_id)
                cache.set(cache_key, item, timeout=60*15)  # Cache for 15 minutes
            except Item.DoesNotExist:
                logger.error(f'Item not found: {item_id}')
                return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item)
        return Response(serializer.data)

class ItemCreate(APIView):
    def post(self, request):
        """
        Create a new item in the inventory.
        """
        name = request.data.get('name')
        description = request.data.get('description')

        if Item.objects.filter(name=name).exists():
            return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if not name or not description:
            return Response({"error": "Both 'name' and 'description' are required."}, status=status.HTTP_400_BAD_REQUEST)

        new_item = Item.objects.create(name=name, description=description)

        return Response({
            "id": new_item.id,
            "name": new_item.name,
            "description": new_item.description,
            "created_at": new_item.created_at,
            "updated_at": new_item.updated_at
        }, status=status.HTTP_201_CREATED)

class ItemUpdate(APIView):
    def put(self, request, item_id):
         """
        Update an existing item in the inventory.
        """
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        description = request.data.get('description')

        if not name or not description:
            return Response({"error": "Both 'name' and 'description' are required."}, status=status.HTTP_400_BAD_REQUEST)

        item.name = name
        item.description = description
        item.save() 

        return Response({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        }, status=status.HTTP_200_OK)

class ItemDelete(APIView):
    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            logger.info(f'Item deleted: {item_id}')
            return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.error(f'Item not found for deletion: {item_id}')
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
