from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('api/v1/users/',views.user_all, name='all_user'),
    path('api/v1/users/create/',views.user_create, name='create_user'),
    path('api/v1/reviews/',views.user_all, name='all_reviews'),
    path('api/v1/reviews/create/',views.user_create, name='create_reviews'),
]