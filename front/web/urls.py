from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('home/',views.home, name='home'),
    path('products/<int:product_id>/',views.product_detail, name='product_detail'),
    path('users/<int:user_id>/',views.user_profile, name='user_profile')
]