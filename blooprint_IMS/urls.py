from django.urls import path
from .views import *
from .authentication import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('items/<int:item_id>/', ItemGet.as_view(), name='item-get'),
    path('items/', ItemCreate.as_view(), name='item-create'),
    path('items/<int:item_id>/', ItemUpdate.as_view(), name='item-update'),
    path('items/<int:item_id>/', ItemDelete.as_view(), name='item-delete'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),  
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('items-list/', ItemList.as_view(), name='item_list'),

]
