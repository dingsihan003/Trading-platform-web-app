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
    auth = request.COOKIES.get('auth')
    if auth:
        auth = 1
    else:
        auth = 0
    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/home/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        context = {
            'price_listing': resp[0],
            'date_listing': resp[1],
            'auth': auth,
        }
        return render(request,'web/home.html',context)
    else:
        return HttpResponse('Error')

def product_detail(request,product_id):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = 1
    else:
        auth = 0
    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/products/'+ str(product_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'product': resp,
            'auth': auth,
        }
        return render(request,'web/products_detail.html',context)
    else:
        return HttpResponse('Error')


def user_profile(request,user_id):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = 1
    else:
        auth = 0

    if request.method == 'GET':
        req = urllib.request.Request('http://experience:8000/users/'+ str(user_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'Users': resp,
            'auth': auth,
        }

        return render(request,'web/user_profile.html',context)
    else:
        return HttpResponse('Error')



@csrf_exempt
def update_profile_email(request,user_id):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = 1
    else:
        auth = 0

    form=emailForm(request.POST)
    if form.is_valid():
        info=form.cleaned_data
        info["email"]=request.POST("email")
        post_encoded = urllib.parse.urlencode(info).encode('utf-8')
        req = urllib.request.Request('http://experience:8000/users/', data=post_encoded, method='POST')
        resp = json.loads(resp_json)
        post_encoded = urllib.parse.urlencode(info).encode('utf-8')
    context = {
            'Users': resp,
            'auth': auth,
        }   
    return render(request,'web/email.html',context)



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
@csrf_exempt
def logout(request):
    auth = request.COOKIES.get('auth')
    logout_dict = {"authenticator": auth}
    logout_encode = urllib.parse.urlencode({"authenticator": auth}).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/logout/', data=logout_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie("auth")
    return response

@csrf_exempt
def create_listing(request):

    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
    # if request.method == 'GET':
    #     return render(request, "web/create_listing.html")
    f = ListingForm(request.POST)
    context = {
            'form': f,
        }  
    if not f.is_valid():
        print("error")
        return render(request, 'web/create_listing.html',context)
    listing = f.cleaned_data
    listing_encode = urllib.parse.urlencode(listing).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/create_listing/', data=listing_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    resp1 = json.loads(resp_json1)

    # # ...

    # # Send validated information to our experience layer
    # resp = create_listing_exp_api(auth, ...)

    # # Check if the experience layer said they gave us incorrect information
    # if resp and not resp['ok']:
    #     if resp['error'] == exp_srvc_errors.E_UNKNOWN_AUTH:
    #         # Experience layer reports that the user had an invalid authenticator --
    #         #   treat like user not logged in
    #         return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing")

    # # ...

    return render(request, "web/create_listing_success.html")

