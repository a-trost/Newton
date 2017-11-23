import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from .models import IXLList


class IXLListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_staff = True
        self.client.login(username='john', password='johnpassword')

    def test_all_lists_view(self):
        resp = self.client.get('/ixl/lists/view')
        self.assertEqual(resp.status_code, 200)
