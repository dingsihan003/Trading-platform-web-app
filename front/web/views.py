from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from urllib.error import URLError
from django.urls import reverse

# import exp_srvc_errors
from .forms import *

# Create your views here.
def home(request):
    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/home/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        context = {
            'price_listing': resp[0],
            'date_listing': resp[1],
        }
        return render(request,'web/home.html',context)
    else:
        return HttpResponse('Error')

def product_detail(request,product_id):
    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/products/'+ str(product_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'product': resp,
        }
        return render(request,'web/products_detail.html',context)
    else:
        return HttpResponse('Error')


def user_profile(request,user_id):

    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/users/'+ str(user_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'Users': resp,
        }

        return render(request,'web/user_profile.html',context)
    else:
        return HttpResponse('Error')



@csrf_exempt
def update_profile_email(request,user_id):
    if request.method == 'POST':
        form=emailForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            info["email"]=request.POST("email")
            post_encoded = urllib.parse.urlencode(info).encode('utf-8')
            print(post_encoded)
            req = urllib.request.Request('http://experience:8000/users/update/' + str(user_id )+ '/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            post_encoded = urllib.parse.urlencode(info).encode('utf-8')
        else:
            return HttpResponse('Invalid Form')
    else:
        req = urllib.request.Request('http://experience:8000/users/'+ str(user_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'Users': resp,
        }
        return render(request,'web/email.html',context)

    return render(request,'web/email.html')



@csrf_exempt
def login(request):
    if request.method == 'GET':
        next = request.GET.get('next') or reverse('home')
        return render(request, 'web/login.html')
    f =  LoginForm(request.POST)
    if not f.is_valid():
      return render(request, 'web/login.html')
      
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    login_dict = {"username": username, "password": password}
    login_encode = urllib.parse.urlencode(login_dict).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/login/', data=login_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    resp = json.loads(resp_json1)

    next = f.cleaned_data.get('next') or reverse('home')
    if (resp_json1 == 'User does not exist or password incorrect.'): 
      return render(request, 'web/login.html')
    authenticator = resp['authenticator']

    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response

def signup(request):
    f =  SignUpForm(request.POST)
    if not f.is_valid():
      return render(request, 'web/signup.html')

    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    location = f.cleaned_data['location']
    email = f.cleaned_data['email']
    signup_dict = {"username": username, "password": password, "location": location, "email": email}
    signup_encode = urllib.parse.urlencode(signup_dict).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/signup/', data=signup_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    resp = json.loads(resp_json1)

    next = f.cleaned_data.get('next') or reverse('home')
    authenticator = resp[1]['authenticator']

    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response

def logout(request):
    auth = request.COOKIES.get('auth')
    logout_dict = {"authenticator": auth}
    logout_encode = urllib.parse.urlencode({"authenticator": auth}).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/signup/', data=logout_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie("auth")
    return response
