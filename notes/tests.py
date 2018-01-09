from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from .models import *
from django.utils import timezone


"""
Note:
    testについて参考:
    https://docs.djangoproject.com/ja/2.0/topics/testing/
"""


class NoteTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.user = User.objects.create(username='test')
        self.user.set_password('password')
        self.user.save()
        self.note1 = Note.objects.create(
            title='test title',
            content='本日は晴天なり',
            locate='location',
            date=timezone.now(),
            start_time=timezone.now(),
            end_time=timezone.now(),
            elapsed_time=10,
            user=self.user,
            text_type=1
        )
        self.note1.tag.add(self.tag1)
        # self.note1.tag.add(self.tag2)

    def tearDown(self):
        self.note1.delete()
        self.tag1.delete()
        self.tag2.delete()
        self.user.delete()

    def test_normal(self):
        notes = Note.objects.all()
        self.assertTrue(self.note1 in notes)

    def test_note_list(self):
        client = APIClient()
        response = client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_detail(self):
        client = APIClient()
        response = client.get('/api/note/' + str(self.note1.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_edit(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        self.assertEqual(self.note1.tag_list(), 'tag1')
        response = client.patch('/api/note/1/update/', {
            "title": "テストだよ",
            "content": "テストだよ",
            "tag": [
                "tag1",
                "tag2"
            ]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user, self.note1.user)
        self.assertEqual(self.note1.tag_list(), 'tag1, tag2')

    def test_note_create_delete(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response_create = client.post('/api/create/note/', {
            'title': 'test note',
            'content': 'こんにちは',
            'locate': 'ここ',
            'date': str(timezone.now().date()),
            'start_time': str(timezone.now()),
            'end_time': str(timezone.now()),
            'elapsed_time': 10,
            'user': self.user.id,
            'text_type': 1,
            'has_metadata': False
        }, format='json')
        response_delete = client.delete('/api/note/2/delete/')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)


class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('password')
        self.user.save()
        self.note = Note.objects.create(
            title='test title',
            content='本日は晴天なり',
            locate='location',
            date=timezone.now(),
            start_time=timezone.now(),
            end_time=timezone.now(),
            elapsed_time=10,
            user=self.user,
            text_type=1
        )
        self.comment = Comment.objects.create(
            name='test',
            content='testtest',
            note=self.note,
            user=self.user,
            anonymous=False,
            posted_date=timezone.now()
        )

    def tearDown(self):
        self.note.delete()
        self.user.delete()
        self.comment.delete()

    def test_comment_create(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response_create = client.post('/api/create/comment/', {
            'name': 'テスト',
            'content': 'テストコメント',
            'note': self.note.id,
            'user': self.user.id,
            'anonymous': False,
            'posted_date': timezone.now()
        }, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    def test_edit_comment(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        self.assertEqual(self.comment.content, 'testtest')
        response = client.patch('/api/comment/1/update/', {
            'content': '編集したよ'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], '編集したよ')

    def test_comment_delete(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response_delete = client.delete('/api/comment/' + str(self.note.id) + '/delete/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
