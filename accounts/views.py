from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import render, redirect
from django.views import View

from .models import User
from api.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            User.objects.create(**ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })