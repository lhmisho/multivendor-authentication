from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VendorCreateSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


class VendorRegisterView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VendorCreateSerializer

    def post(self, request):
        if not request.user.is_owner:
            return Response({"error": ["Only shop owner can create Vendor!", ]}, status=status.HTTP_400_BAD_REQUEST)
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data.parent = request.user
        data.created_by = request.user
        data.updated_by = request.user
        data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
