from django.test import TestCase, Client
from django.urls import reverse
from .models import Users, Product, Review

class UsersTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass #nothing to set up

    def TestReadingUser(self):
        response = self.client.get(reverse('all_users', kwargs={'user_id':1}))
        self.assertContains(response, 'all_users')

    def TestCreateUser(self):
        


    def tearDown(self):
        pass #nothing to tear down