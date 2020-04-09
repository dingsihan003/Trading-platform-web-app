from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.error import URLError
from django.core.mail import send_mail
from django.conf import settings
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


producer = KafkaProducer(bootstrap_servers='kafka:9092')
producer_log = KafkaProducer(bootstrap_servers='kafka:9092')
es = Elasticsearch(['es']) 

# Create your views here.
@csrf_exempt
def get_search_result(request):
  if request.method == "GET":
    query = request.GET.get("query")
    es_resp = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
    resp =  es_resp['hits']['hits']
    results = sorted(resp, key=lambda k:k['_score'], reverse = True)
    results_source = [result['_source'] for result in results]
    return JsonResponse({"results":results_source},safe=False)
  if request.method == 'POST':
    return HttpResponse('Error')

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


@csrf_exempt 
def profile_update(request,user_id):
    if request.method == "POST":
        res=(request.POST).dict()
        res_encode = urllib.parse.urlencode(res).encode('utf-8')
        req1= urllib.request.Request('http://models:8000/api/v1/users/update/' + str(user_id )+ '/', data=res_encode, method='POST')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)

        return JsonResponse(resp1, safe=False)
    else:
        return HttpResponse('Error')

def name_user_get(request,user_name):
    if request.method == 'GET':
        req = urllib.request.Request('http://models:8000/api/v1/users/name/'+ user_name + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        try:
            resp = json.loads(resp_json)
            return JsonResponse(resp, safe=False)
        except:
            return HttpResponse('Error')
    else:
        return HttpResponse('Error')

         
@csrf_exempt 
def signup(request):
    if request.method == "POST":
        res1 = (request.POST).dict()
        res_encode = urllib.parse.urlencode(res1).encode('utf-8')
        req1 = urllib.request.Request('http://models:8000/api/v1/users/create/', data=res_encode, method='POST')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        try:
            resp1 = json.loads(resp_json1)
        except:
            return JsonResponse([False,False], safe=False)

        username_encode = urllib.parse.urlencode({"username": request.POST["username"]}).encode('utf-8')
        req2 = urllib.request.Request('http://models:8000/api/v1/authenticator/create/', data=username_encode, method='POST')
        resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
        resp2 = json.loads(resp_json2)

        return JsonResponse([resp1,resp2], safe=False)
    else:
        return HttpResponse('Error')

@csrf_exempt 
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
@csrf_exempt
def logout(request):
    if request.method == "POST":
        req1 = urllib.request.Request('http://models:8000/api/v1/authenticator/find/'+ request.POST["authenticator"] + '/')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)        
        req2 = urllib.request.Request('http://models:8000/api/v1/authenticator/delete/'+ str(resp1["authenticator"]+'/'), method='DELETE')
        resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
        return HttpResponse('Deleted')
    else:
        return HttpResponse('Error')

@csrf_exempt       
def create_listing(request):
    if request.method == "POST":
        res = (request.POST).dict()
        listing_encode = urllib.parse.urlencode(res).encode('utf-8')
        req1 = urllib.request.Request('http://models:8000/api/v1/products/create/', data=listing_encode, method='POST')
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        resp1 = json.loads(resp_json1)
        print(resp1)
        res['id'] = resp1['id']
        print(res)
        producer.send('listing', json.dumps(res).encode('utf-8'))
        return JsonResponse(resp1, safe=False)
    else:
        return HttpResponse('Error')

@csrf_exempt  
def forget_password(request):
    if request.method == "POST":
        res = (request.POST).dict()
        listing_encode = urllib.parse.urlencode(res).encode('utf-8')
        req1 = urllib.request.Request('http://models:8000/api/v1/users/find/', data = listing_encode, method="POST")
        resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
        if resp_json1 == "Valid":
            req2 = urllib.request.Request('http://models:8000/api/v1/forget/',data = listing_encode, method="POST")
            resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
            resp2 = json.loads(resp_json2)
            subject = "Reset Password"
            message = "Please go to http://127.0.0.1:8000/reset_password/"+ str(resp2['active_code'])+ "/ to reset your password"
            send_mail(subject, message,'isamarketplace2020@gmail.com', [resp2['email']])

            return JsonResponse(resp2, safe=False)
        else:
            return HttpResponse("User does not exist")

    else:
        return HttpResponse('Error')
@csrf_exempt 
def reset_password(request,active_code):
    if request.method == "POST":
        res = (request.POST).dict()
        password_encode = urllib.parse.urlencode(res).encode('utf-8')
        try:
            req1 = urllib.request.Request('http://models:8000/api/v1/reset/'+str(active_code)+'/', data=password_encode, method='POST')
            resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
            resp1 = json.loads(resp_json1)
            return JsonResponse(resp1, safe=False)
        except:
            return HttpResponse('Error')

    else:
        return HttpResponse('Error')




