from django.test import TestCase, Client
from django.urls import reverse
from .models import Users, Product, Review
import urllib.request
import urllib.parse
import json

class UsersTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass #nothing to set up

    def testReadingUser(self):
        response = self.client.get(reverse('all_user', kwargs={'id':1}))
        self.assertContains(response, 'all_user')

    def testCreateUser(self):
        post_data = {'username': 'Demo User', 'email': 'example@a.com', 'location': 'VA'}
        self.client.post(post_data)
        
        test = self.client.get(reverse('all_user', kwargs={'email':'example@a.com'}))

        self.assertContains(test,'all_user')