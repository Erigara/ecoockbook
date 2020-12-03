from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from .views import RegistrationView, LoginView, LogoutView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    # path('login', LoginView.as_view(), name='login'),
    # path('logout', LogoutView.as_view(), name='logout'),
]