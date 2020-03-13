from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('home/',views.home, name='home'),
    path('products/<int:product_id>/',views.product_detail, name='product_detail'),
    path('users/<int:user_id>/',views.user_profile, name='user_profile'),
    path('users/<int:user_id>/update/',views.user_profile, name='user_profile'),

    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.signup, name='logout'),

    path('users/<int:user_id>/',views.user_profile, name='user_profile')
]