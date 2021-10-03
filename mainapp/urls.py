from django.urls import path
from .views import index, signup, date_details, create_booking, delete_booking

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('date_details/', date_details, name='date_details'),
    path('create_booking/', create_booking, name='create_booking'),
    path('delete_booking/', delete_booking, name='delete_booking'),
]