from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VendorCreateSerializer


class VendorRegisterView(generics.GenericAPIView):
    serializer_class = VendorCreateSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data.parent = request.user
        data.created_by = request.user
        data.updated_by = request.user
        return Response(data, status=status.HTTP_200_OK)
