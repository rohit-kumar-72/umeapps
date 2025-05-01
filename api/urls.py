from django.urls import path
from core.views import analyze

urlpatterns = [
    path('', analyze),
]
