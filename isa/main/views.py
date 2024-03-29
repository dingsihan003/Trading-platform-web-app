from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from .models import *
from django.forms.models import model_to_dict
import os
import hmac
from django.contrib.auth import hashers
from django.utils import timezone
import datetime
import random
import json
# Create your views here.

# AUTHENTICATOR
@csrf_exempt
def create_authenticator(request):
    if request.method == 'POST':
        json_data = request.POST
        auth = Authenticator()
        for k, v in json_data.items():
            setattr(auth, k, v)
        authenticator = hmac.new(
        key = settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256',
        ).hexdigest()
        auth.authenticator = authenticator
        auth.date_created = timezone.now()
        auth.save()
        return JsonResponse(model_to_dict(auth))
    else:
        return HttpResponse("Error")
@csrf_exempt
def find_authenticator(request, authenticator):
    if request.method == 'GET':
        try:
            auth = Authenticator.objects.get(authenticator = authenticator)
        except:
            return HttpResponse("Authenticator does not exist")
        if auth.date_created <= timezone.now() - datetime.timedelta(days=7):
            return HttpResponse("Authenticator does not exist")
        return JsonResponse(model_to_dict(auth))
    else:
        return HttpResponse("Error")
@csrf_exempt
def delete_authenticator(request, authenticator):
    if request.method == 'DELETE':
        try:
            auth = Authenticator.objects.get(authenticator = authenticator)
        except:
            return HttpResponse("Authenticator does not exist")
        auth.delete()
        return HttpResponse("Auth deleted")
    else:
        return HttpResponse("Error")


# USER SECTION

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        json_data = request.POST
        user = Users()
        for k, v in json_data.items():
            if k == 'password':
                setattr(user, k, hashers.make_password(json_data['password']))
            else:
                setattr(user, k, v)
        try:
            Users.objects.get(username=user.username)
            Users.objects.get(email=user.email)
            return HttpResponse("ERROR: Username or email already registered")
        except:
            user.save()
            return JsonResponse(model_to_dict(user))
    else:
        return HttpResponse("Error")

@csrf_exempt
def all_user(request):
    if request.method == 'GET':
        users = Users.objects.all()
        all_users = []
        for i in users:
            all_users.append(model_to_dict(i))
        return JsonResponse(all_users, safe=False)
    else:
        return HttpResponse("error")
@csrf_exempt
def user(request,user_id):
    if request.method == 'GET':
        users = Users.objects.get(pk=user_id)
        return JsonResponse(model_to_dict(users))
    else:
        return HttpResponse("error")
@csrf_exempt
def name_user_get(request,user_name):
    if request.method == 'GET':
        try:
            users = Users.objects.get(username=user_name)
            return JsonResponse(model_to_dict(users))
        except:
            return HttpResponse("User does not exist")
    else:
        return HttpResponse("error")

@csrf_exempt
def find_user(request):
    if request.method == 'POST':
        try:
            user = Users.objects.get(username=request.POST['username'])
            return HttpResponse("Valid")
        except:
            return HttpResponse("Invalid")
    else:
        return HttpResponse("Error")

        
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'POST':
        json_data = request.POST
        users = Users.objects.get(pk=user_id)
        if 'email' in json_data:
            users.email = json_data['email']
        if 'location' in json_data:
            users.location = json_data['location']

        try:
            users.save()
            return JsonResponse(model_to_dict(users))
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")

@csrf_exempt
def check_user(request):
    if request.method == 'POST':
        try:
            user = Users.objects.get(username=request.POST['username'])
        except:
            return HttpResponse("Invalid")
        if hashers.check_password(request.POST['password'], user.password):
            return HttpResponse("Valid")
        else:
            return HttpResponse("Invalid")
    else:
        return HttpResponse("Error")
@csrf_exempt
def code_RQ(codelength=8):
    code=''
    str='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    str_len=len(str)-1
    for i in range(codelength):
        code+=str[random.randint(0,str_len)]
    return code

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        user = Users.objects.get(username=request.POST['username'])
        try:
            codeObj=Code.objects.get(email=user.email)
            codeObj.active_code=code_RQ()

        except:
            codeObj= Code()
            codeObj.email = user.email
            codeObj.active_code = code_RQ()
        try:
            codeObj.save()
            return JsonResponse(model_to_dict(codeObj))
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")
@csrf_exempt
def reset_password(request,active_code):
    if request.method == 'POST':
        try:
            code = Code.objects.get(active_code = active_code)
            user = Users.objects.get(email=code.email)
            print("ccc")
            setattr(user, 'password', hashers.make_password(request.POST['password']))
        except:
            return HttpResponse("error")

        try:
            user.save()
            return JsonResponse(model_to_dict(user))
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")

# PRODUCT SECTION

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        json_data = request.POST
        product = Product()
        for k, v in json_data.items():
            setattr(product, k, v)
        try:
            product.save()
            return JsonResponse(model_to_dict(product),safe=False)
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")

def all_product(request):
    if request.method == 'GET':
        products = Product.objects.all()
        all_products = []
        for i in products:
            all_products.append(model_to_dict(i))
        return JsonResponse(all_products , safe=False)
    else:
        return HttpResponse("error")

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        Product.objects.get(pk=product_id).delete()
        return HttpResponse("Product" + str(product_id) + "has been deleted")
    else:
        return HttpResponse("error")

def product_detail(request, product_id):
    if request.method == "GET":
        product = Product.objects.get(pk=product_id)
        return JsonResponse(model_to_dict(product))
    else:
        return HttpResponse("error")

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        json_data = request.POST
        product = Product.objects.get(pk=product_id)
        if 'product_base_price' in json_data:
            product.product_base_price = json_data['product_base_price']
        if 'product_description' in json_data:
            product.product_description = json_data['product_description']
        if 'sold' in json_data:
            product.sold = json_data['sold']
        if 'product_date_added' in json_data:
            return HttpResponse("You cannot update product added date.")
        try:
            product.save()
            return JsonResponse(model_to_dict(product))
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")

def price_listing(request):
    if request.method == 'GET' :
        products = Product.objects.all().order_by('product_base_price')
        all_products = []
        for i in products:
            all_products.append(model_to_dict(i))
        return JsonResponse(all_products , safe=False)
    else:
        return HttpResponse("error")

def date_listing(request):
    if request.method == 'GET' :
        products = Product.objects.all().order_by('product_date_added')
        all_products = []
        for i in products:
            all_products.append(model_to_dict(i))
        return JsonResponse(all_products , safe=False)
    else:
        return HttpResponse("error")

# REIVEW SECTION

@csrf_exempt
def post_review(request):
    if request.method == 'POST':
        json_data = request.POST
        review = Review()
        if 'title' in json_data:
            review.title = json_data['title']
        if 'text' in json_data:
            review.text = json_data['text']
        if 'review_date_added' in json_data:
            return HttpResponse("You cannot set review added date.")
        if 'poster' in json_data:
            try:
                review.poster = Users.objects.get(pk=json_data['poster'])
            except:
                return HttpResponse("Invalid Input")
        if 'postee' in json_data:
            try:
                review.postee = Users.objects.get(pk=json_data['postee'])
            except:
                return HttpResponse("Invalid Input")
        try:
            review.save()
            return JsonResponse(model_to_dict(review))
        except:
            return HttpResponse("Invalid Input or poster / postee cannot be empty ")
    else:
        return HttpResponse("error") 

def all_review(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        all_reviews = []
        for i in reviews:
            all_reviews.append(model_to_dict(i))
        return JsonResponse(all_reviews, safe=False)
    else:
        return HttpResponse("error")

@csrf_exempt
def delete_review(request, review_id):
    if request.method == 'DELETE':
        Review.objects.get(pk=review_id).delete()
        return HttpResponse("Review" + str(review_id) + "has been deleted")
    else:
        return HttpResponse("error")

@csrf_exempt
def update_review(request, review_id):
    if request.method == 'POST':
        json_data = request.POST
        reviews = Review.objects.get(pk=review_id)
        if 'title' in json_data:
            reviews.title = json_data['title']
        if 'text' in json_data:
            reviews.text = json_data['text']
        if 'poster' in json_data:
            return HttpResponse("You cannot update poster.")
        if 'postee' in json_data:
            return HttpResponse("You cannot update postee.")
        if 'review_date_added' in json_data:
            return HttpResponse("You cannot update review added date.")
        try:
            reviews.save()
            return JsonResponse(model_to_dict(reviews))
        except:
            return HttpResponse("Invalid Input")
    else:
        return HttpResponse("error")

@csrf_exempt
def create_recommendation(request):
    if request.method == 'POST':
        recommendations = json.loads(request.POST.copy().get("recommendations"))
        if len(recommendations) == 0: 
            return HttpResponse("No recommendations available")
        Recommendation.objects.all().delete()
        for k, v in recommendations.items():
            Recommendation.objects.create(item_id=int(k), recommended_items=v)
        return HttpResponse("Recommendations created successfully")
    else:
        return HttpResponse("error")

@csrf_exempt
def get_recommendation(request, pk):
    if request.method == "GET":
        try:
            recommendation = Recommendation.objects.get(item_id = pk)
        except Recommendation.DoesNotExist:
            return JsonResponse({"item_id": pk, "recommended_items":[]})
        except:
            return HttpResponse("recommendation does not exist")
        recommendation_dict = model_to_dict(recommendation)
        recommendation_dict['recommended_items'] = recommendation_dict['recommended_items'].split(',')
        return JsonResponse(recommendation_dict)
    else:
        return HttpResponse("error")

