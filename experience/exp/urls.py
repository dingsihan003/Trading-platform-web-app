from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('home/',views.home, name='home'),
    path('products/<int:product_id>/',views.product_detail, name='product_detail'),
    path('users/<int:user_id>/',views.user_profile, name='user_profile'),
    path('users/name/<str:user_name>/',views.name_user_get, name='user_name'),
    path('users/update/<int:user_id>/',views.profile_update, name='profile_update'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('signup/',views.signup, name='signup'),
    path('create_listing/',views.create_listing, name='create_listing'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_password/<str:active_code>/',views.reset_password, name='reset_password'),
    path('get_search_result/', views.get_search_result, name="get_search_result"),
    path('get_pop_search_result/', views.get_pop_search_result, name="get_pop_search_result"),
]