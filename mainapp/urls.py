from django.urls import path
from django.conf.urls import url
# separate long import need ()
from .views import (
    index, signup, date_details, create_booking,
    delete_booking, change_profile, change_password
)

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('date_details/', date_details, name='date_details'),
    path('create_booking/', create_booking, name='create_booking'),
    path('delete_booking/', delete_booking, name='delete_booking'),
    path('change_profile/', change_profile, name='change_profile'),
    url(r'^password/$', change_password, name='change_password'),
]