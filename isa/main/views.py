from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.forms.models import model_to_dict
# Create your views here.


# USER SECTION

@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        json_data = request.POST
        user = Users()
        for k, v in json_data.items():
            setattr(user, key, value)
        user.save()
        return JsonResponse(model_to_dict(user),safe=False)
    else:
        return HttpResponse("error")


def user_all(request):
    if request.method == 'GET':
        users = Users.objects.all()
        usersList = []
        for i in users:
            usersList.append(model_to_dict(i))
        return JsonResponse(usersList, safe=False)
    else:
        return HttpResponse("error")

# PRODUCT SECTION

@csrf_exempt
def prodcut_create(request):
    if request.method == 'POST':
        json_data = request.POST
        product = Product()
        for k, v in json_data.items():
            setattr(product, key, value)
        product.save()
        return JsonResponse(model_to_dict(product),safe=False)
    else:
        return HttpResponse("error")

def product_all(request):
    if request.method == 'GET':
        products = Product.objects.all()
        ProductList = []
        for i in products:
            ProductList.append(model_to_dict(i))
        return JsonResponse(ProductList, safe=False)
    else:
        return HttpResponse("error")

def delete_product(request, product_id):
    if request.method == 'DELETE':
        Product.objects.get(pk=product_id).delete()
        return HttpResponse("Product" + str(review_id) + "has been deleted")
    else:
        return HttpResponse("error")

@csrf_exempt
def update_product(request, review_id):
    if request.method == 'POST':
        json_data = request.POST
        product = Product.objects.get(pk=product_id)
        if 'product_title' in json_data:
            product.title = json_data['product_title']
        if 'product_base_price' in json_data:
            product.title = json_data['product_base_price']
        if 'product_description' in json_data:
            product.title = json_data['product_description']
        if 'sold' in json_data:
            product.title = json_data['sold']
        if 'product_date_added' in json_data:
            return HttpResponse("You cannot update product added date.")
        product.save()
        return JsonResponse(model_to_dict(product))
    else:
        return HttpResponse("error")

# REIVEW SECTION

@csrf_exempt
def post_review(request):
    if request.method == 'POST':
        json_data = request.POST
        review = Review()
        for k, v in json_data.items():
            setattr(review, key, value)
        if 'poster' in json_data:
            reviewObj.poster_user = Users.objects.get(pk=json_data['poster'])
        if 'postee' in json_data:
            reviewObj.postee_user = Users.objects.get(pk=json_data['postee'])
        review.save()
        return JsonResponse(model_to_dict(reviewObj))
    else:
        return HttpResponse("error") 

def all_review(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        reviewsList = []
        for i in reviews:
            reviewsList.append(model_to_dict(i))
        return JsonResponse(reviewsList, safe=False)
    else:
        return HttpResponse("error")

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
            reviews.title = json_data['text']
        if 'poster' in json_data:
            return HttpResponse("You cannot update poster.")
        if 'postee' in json_data:
            return HttpResponse("You cannot update postee.")
        reviews.save()
        return JsonResponse(model_to_dict(reviews))
    else:
        return HttpResponse("error")
