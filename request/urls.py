from django.urls import re_path, path, include
from .views import *
urlpatterns = [
    path('get_regions', get_regions),
    path('add', get_id_search),
    path('stat', get_request),
]