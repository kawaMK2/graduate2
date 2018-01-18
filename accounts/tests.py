from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from .models import *

"""
Note:
    testについて参考:
    https://docs.djangoproject.com/ja/2.0/topics/testing/
"""


# Grade test
class GradeTest(TestCase):
    def setUp(self):
        self.grade1 = Grade.objects.create(name='grade1', formal_name='Grade 1', priority=100)
        self.grade2 = Grade.objects.create(name='grade2', formal_name='Grade 2', priority=10)

    def tearDown(self):
        self.grade1.delete()
        self.grade2.delete()

    def test_normal(self):
        before = Grade.objects.all()
        self.assertTrue(self.grade1 in before)
        self.assertTrue(self.grade2 in before)

    def test_grade_list(self):
        client = APIClient()
        response = client.get('/api/grades/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_detail(self):
        client = APIClient()
        response = client.get('/api/grade/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'grade1')


# User test
class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test',
            first_name='太郎',
            last_name='テスト'
        )

    def tearDown(self):
        self.user.delete()

    def test_normal(self):
        users = User.objects.all()
        self.assertTrue(self.user in users)

    def test_full_name(self):
        self.assertTrue(self.user.get_full_name() == 'テスト 太郎')

    def test_user_edit(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch('/api/user/' + self.user.username + '/update/', {
            "first_name": "変更"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Belong test
class BelongTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='テスト',
            first_name='太郎',
            last_name='テスト',
        )
        self.admin = User.objects.create(
            username='admin',
            first_name='太郎',
            last_name='管理者',
            is_superuser=True
        )
        self.grade = Grade.objects.create(
            name='テスト年',
            formal_name='テスト 年次',
            priority=10
        )
        self.belong = Belong.objects.create(
            user=self.user,
            grade=self.grade,
            start=timezone.now()
        )

    def tearDown(self):
        self.belong.delete()
        self.user.delete()
        self.grade.delete()

    def test_normal(self):
        belongs = Belong.objects.all()
        self.assertTrue(self.grade in self.user.belongs.all())
        self.assertTrue(self.belong in belongs)
