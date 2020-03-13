from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.error import URLError
# import exp_srvc_errors
# from .forms import *

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



def login(request):
    if request.method == 'GET':
        next = request.GET.get('next') or reverse('home')
        return render(request, 'login.html')
    f =  LoginForm(request.POST)
    if not f.is_valid():
      return render(request, 'login.html')

    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    login_dict = {"username": username, "password": password}
    login_encode = urllib.parse.urlencode(login_dict).encode('utf-8')
    req1 = urllib.request.Request('http://experience:8000/login/', data=login_encode, method='POST')
    resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
    resp = json.loads(resp_json1)

    next = f.cleaned_data.get('next') or reverse('home')
    if (resp_json1 == 'User does not exist or password incorrect.'): 
      return render(request, 'login.html')
    authenticator = resp['authenticator']

    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response
    