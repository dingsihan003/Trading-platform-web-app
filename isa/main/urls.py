from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    path('api/v1/users/',views.user_all, name='user_all'),
    path('api/v1/users/create/',views.user_create, name='user_create'),
    path('api/v1/products/',views.product_all, name='product_all'),
    path('api/v1/reviews/',views.all_review, name='all_reviews'),
    path('api/v1/reviews/create/',views.post_review, name='create_reviews'),

]