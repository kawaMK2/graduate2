from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import *
from .models import *
from .serializers import *
from .permissions import *


"""     Note関連APIView       """


class NotesListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, title='My title')


class NoteUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


"""     Tag関連APIView        """


class TagListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'name'


class TagDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'name'


class TagDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'name'


"""     Comment関連APIView        """


class CommentListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
