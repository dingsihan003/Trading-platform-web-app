from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.forms.models import model_to_dict
# Create your views here.


# USER SECTION

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        json_data = request.POST
        user = Users()
        for k, v in json_data.items():
            setattr(user, k, v)
        try:
            user.save()
            return JsonResponse(model_to_dict(user),safe=False)
        except:
            return HttpResponse("Invalid Input or product_title / product_base_price / product_description cannot be empty")
    else:
        return HttpResponse("Error")


def all_user(request):
    if request.method == 'GET':
        users = Users.objects.all()
        all_users = []
        for i in users:
            all_users.append(model_to_dict(i))
        return JsonResponse(all_users, safe=False)
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

def price_listinng(request):
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
