from django.urls import path
from .views import *

urlpatterns = [
	path('notes/', NotesListAPIView.as_view()),
	path('notes/<username>/', UserNotesListAPIView.as_view()),
	path('note/<pk>/', NoteDetailAPIView.as_view()),
	path('note/<pk>/update/', NoteUpdateAPIView.as_view()),
	path('note/<pk>/delete/', NoteDeleteAPIView.as_view()),
	path('create/note/', NoteCreateAPIView.as_view()),
	path('tags/', TagListAPIView.as_view()),
	path('tag/<name>/', TagDetailAPIView.as_view()),
	path('tag/<name>/delete/', TagDeleteAPIView.as_view()),
	path('create/tag/', TagCreateAPIView.as_view()),
	path('comments/', CommentListAPIView.as_view()),
	path('comment/<pk>/', CommentDetailAPIView.as_view()),
	path('comment/<pk>/update/', CommentUpdateAPIView.as_view()),
	path('comment/<pk>/delete/', CommentDeleteAPIView.as_view()),
	path('create/comment/', CommentCreateAPIView.as_view()),
]
