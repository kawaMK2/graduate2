from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import *


"""
Note:
    参考：
    https://qiita.com/xKxAxKx/items/60e8fb93d6bbeebcf065
"""

urlpatterns = [
    path('auth/login/', obtain_jwt_token),
    path('register/', AuthRegisterAPIView.as_view()),
    path('user/<username>/', AuthDetailAPIView.as_view()),
    path('user/<username>/update/', AuthUpdateAPIView.as_view()),
    path('user/<username>/delete/', AuthDeleteAPIView.as_view()),
    path('users/', AuthListAPIView().as_view()),
    path('grades/', GradeListAPIView.as_view()),
    path('grade/<pk>/', GradeDetailAPIView.as_view()),
]
