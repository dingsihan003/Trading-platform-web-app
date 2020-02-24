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
        req = urllib.request.Request('http://experience:8000/home/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return render(request,'web/products_detail.html',context)