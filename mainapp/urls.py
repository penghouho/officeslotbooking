from django.urls import path
from .views import index, signup, date_details

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('date_details/', date_details, name='date_details'),
]