from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from datetime import datetime
from django.db import models
import urllib.request
import urllib.parse
import json
from django.contrib.auth import hashers


class UsersTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        Users.objects.create(username='Example',email='root@v.com',location='Earth',password='pbkdf2_sha256$150000$ulrQ4Wh5Ly3r$2NCd/FE6+uhE/61smUvskDOSpNUS8qFwkgrjvXZvYm8=')
        Users.objects.create(username='Root',email='s@v.com',location='Moon')

    def testReadingUser1(self):
        response = self.client.get('/api/v1/users/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[0].get('username'),"Example")
    
    def testReadingUser2(self):
        response = self.client.get('/api/v1/users/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[1].get('location'),"Moon")

    def testCreateUser1(self):
        response=self.client.post('/api/v1/users/create/',{'username': 'Demo User', 'email': 'example@a.com', 'location': 'VA' , 'password' : '123456'})
        
        data= json.loads(response.content.decode('utf-8'))

        self.assertEqual(data.get('username'),"Demo User")

    def testCreateUser2(self):
        self.client.post('/api/v1/users/create/',{'username': 'Demo User', 'email': 'example@a.com', 'location': 'VA' , 'password' : '123456'})
        response=self.client.post('/api/v1/users/create/',{'username': 'Demo User', 'email': 'example@a.com', 'location': 'VA' , 'password' : '123456'})
        
        self.assertEqual(response.status_code,200)

    def testCheckUser(self):
        response=self.client.post('/api/v1/users/check/',{'username': 'Example', 'password' : '1'})
        self.assertEqual(response.content,b'Invalid')


    def tearDown(self):
        Users.objects.all().delete()

class productTest(TestCase):
    def setUp(self):
        datetime_str = '2016-10-03T19:00:00.999Z'
        datetime_object1 = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        datetime_str2 = '2020-07-03T19:00:00.999Z'
        datetime_object2 = datetime.strptime(datetime_str2, "%Y-%m-%dT%H:%M:%S.%fZ")

        Product.objects.create(product_title='Example',product_base_price=12,product_description='AAA',product_date_added=datetime_object1,sold=False)
        Product.objects.create(product_title='Apple',product_base_price=5,product_description='Bad Apple',product_date_added=datetime_object2,sold=True)

    def testReadingProduct1(self):
        response = self.client.get('/api/v1/products/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[0].get('product_title'),"Example")

    
    def testReadingProduct2(self):
        response = self.client.get('/api/v1/products/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[1].get('product_base_price'),'5.00')

    def testCreatingProduct(self):
        self.client.post('/api/v1/products/create/',{'product_title': 'Phone', 'product_base_price': 999, 'product_description': 'Used'})
        response = self.client.get('/api/v1/products/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[2].get('product_title'),"Phone")
        self.assertEqual(data[2].get('product_base_price'),"999.00")


    # def testUpdatingProduct(self):
    #     self.client.post('/api/v1/products/update/8/',{'product_base_price': 2,'product_description': 'Used'})
    #     response = self.client.get('/api/v1/products/')
    #     data= json.loads(response.content.decode('utf-8'))
    #     print(data)
    #     self.assertEqual(data[0].get('product_base_price'),'2.00')
    #     self.assertEqual(data[0].get('product_description'),'Used')

    def testPriceListing(self):
        response = self.client.get('/api/v1/pricelisting/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(float(data[0].get("product_base_price"))<float(data[1].get("product_base_price")),True)


    def testDateListing(self):
        response = self.client.get('/api/v1/datelisting/')
        data= json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[0].get("product_date_added")<data[1].get("product_date_added"),True)

    
    def tearDown(self):
        Product.objects.all().delete()


class ForgetPassword(TestCase):
    def setUp(self):
        Users.objects.create(username='Example',email='root@v.com',location='Earth',password='pbkdf2_sha256$150000$AiT59lXJSh83$PvKyfutyzDK/5p99JrfHgTuewpSKfxJUwlv1ybG3NS8')

    def testForget(self):
        response=self.client.post('/api/v1/forget/', {'username' : 'Example'})
        self.assertEqual(response.status_code,200)
