from django.urls import path
from .views import VendorRegisterView, UserRegisterView, LoginApiView


urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register-user/', UserRegisterView.as_view(), name='register-user'),
    path('register-vendor/', VendorRegisterView.as_view(), name='register-vendor'),
]
