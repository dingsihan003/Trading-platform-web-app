from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.error import URLError

# Create your views here.
def home(request):
    if request.method == 'GET':
        req1 = urllib.request.Request('http://models:8000/api/v1/pricelisting/')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)
        
        req2 = urllib.request.Request('http://models:8000/api/v1/datelisting/')
        resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
        resp2 = json.loads(resp_json2)

        return JsonResponse([resp1, resp2],safe=False)
    else:
        return HttpResponse('Error')

def product_detail(request,product_id):
    if request.method == 'GET':
        req = urllib.request.Request('http://models:8000/api/v1/products/'+ str(product_id )+ '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp, safe=False)
    else:
        return HttpResponse('Error')

def user_profile(request,user_id):
    if request.method == 'GET':
        req = urllib.request.Request('http://models:8000/api/v1/users/'+ str(user_id )+ '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp, safe=False)
    else:
        return HttpResponse('Error')

def signup(request):
    if request.method == "POST":
        res = (request.POST).dict()
        res_encode = urllib.parse.urlencode(res).encode('utf-8')
        req1 = urllib.request.Request('http://models:8000/api/v1/users/create/', data=res_encode, method='POST')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)

        username_encode = urllib.parse.urlencode({"username": request.POST["username"]}).encode('utf-8')
        req2 = urllib.request.Request('http://models:8000/api/v1/authenticator/create/', data=username_encode, method='POST')
        resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
        resp2 = json.loads(resp_json2)

        return JsonResponse([resp1,resp2], safe=False)
    else:
        return HttpResponse('Error')


def login(request):
    if request.method == "POST":
        res = (request.POST).dict()
        res_encode = urllib.parse.urlencode(res).encode('utf-8')
        req1 = urllib.request.Request('http://models:8000/api/v1/users/check/', data=res_encode, method='POST')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')

        if resp_json1 == 'Valid':
            username_encode = urllib.parse.urlencode({"username": request.POST["username"]}).encode('utf-8')
            req2 = urllib.request.Request('http://models:8000/api/v1/authenticator/create/', data=username_encode, method='POST')
            resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
            resp2 = json.loads(resp_json2)
            return JsonResponse(resp2, safe=False)
        else:
            return HttpResponse('User does not exist or password incorrect.')
    else:
        return HttpResponse('Error')

def logout(request):
    if request.method == "POST":
        req1 = urllib.request.Request('http://models:8000/api/v1/authenticator/find/'+ request.POST["authenticator"] + '/')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)
        
        req2 = urllib.request.Request('http://models:8000/api/v1/authenticator/delete/'+ str(resp1["authenticator"]), method='DELETE')
        resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
        return HttpResponse('Deleted')
    else:
        return HttpResponse('Error')

        
        

