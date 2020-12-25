from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import RegistrationView, LoginView, LogoutView, UserViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
