from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item  # Import your Item model

# Register your Item model with the admin site
@admin.register(Item)  # Using the decorator
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)