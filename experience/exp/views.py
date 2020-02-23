from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.method == 'GET':
        req1 = urllib.request.Request('http://models:8000/api/v1/pricelisting/')
        resp_json1 = urllib.request.urlopen(req).read().decode('utf-8')
        resp1 = json.loads(resp_json1)

        req2 = urllib.request.Request('http://models:8000/api/v1/datelisting/')
        resp_json2 = urllib.request.urlopen(req).read().decode('utf-8')
        resp2 = json.loads(resp_json2)

        return JsonResponse([req1,req2],safe=False)
    else:
        return HttpResponse('Error')

def product_detail(request,product_id):
    if request.method == 'GET':
        req = urllib.request.Request('http://models:8000/api/v1/products/'+ product_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp, safe=False)
    else:
        return HttpResponse('Error')