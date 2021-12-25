from django.urls import path
from .views import VendorRegisterView


urlpatterns = [
    path('register-vendor/', VendorRegisterView.as_view(), name='register-vendor'),
]
