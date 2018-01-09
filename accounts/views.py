from django.contrib.auth import authenticate
from rest_framework import authentication, generics
from rest_framework.permissions import *
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.db import transaction
from django.http import HttpResponse, Http404

from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .serializers import *
from .models import *
from .permissions import *


"""     User関連APIView       """


class AuthRegisterAPIView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class AuthUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnAccountOrReadOnly)
    serializer_class = UserSerializer
    lookup_field = 'username'
    queryset = User.objects.all()


class AuthDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    lookup_field = 'username'
    queryset = User.objects.all()

    def get_object(self):
        try:
            return self.queryset.get(username=self.request.user)
        except User.DoesNotExist:
            raise Http404


class AuthListAPIView(generics.ListAPIView):
    permission_classes = (IsOwnAccountOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


"""     Grade関連APIView       """
# CreateとEditとDeleteはAPIとしては提供しない


class GradeListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()


class GradeDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
