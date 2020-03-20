from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('home/',views.home, name='home'),
    path('products/<int:product_id>/',views.product_detail, name='product_detail'),
    path('users/<int:user_id>/',views.user_profile, name='user_profile'),
    path('users/<int:user_id>/update/email/',views.update_profile_email, name='update_profile_email'),
    path('users/<int:user_id>/update/location/',views.update_profile_location, name='user_profile'),

    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout, name='logout'),
    path('create_listing/',views.create_listing, name='create_listing'),
    path('forget_password/',views.forget_password, name='forget_password'),

    path('users/<int:user_id>/',views.user_profile, name='user_profile')
]