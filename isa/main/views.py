from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.forms.models import model_to_dict
# Create your views here.

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


def product_all(request):
    if request.method == 'GET':
        products = Product.objects.all()
        ProductList = []
        for i in products:
            ProductList.append(model_to_dict(i))
        return JsonResponse(ProductList, safe=False)
    else:
        return HttpResponse("error")
