from django.urls import path
from myapp2.views import search

urlpatterns = [
    path('', search, name='search'),
]