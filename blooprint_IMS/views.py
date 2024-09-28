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
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Item created: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning('Item creation failed: {}'.format(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemUpdate(APIView):
    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.error(f'Item not found for update: {item_id}')
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Item updated: {serializer.data}')
            return Response(serializer.data)
        logger.warning('Item update failed: {}'.format(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDelete(APIView):
    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            logger.info(f'Item deleted: {item_id}')
            return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f'Item not found for deletion: {item_id}')
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
