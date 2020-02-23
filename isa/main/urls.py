from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    path('api/v1/users/',views.all_user, name='all_user'),
    path('api/v1/users/create/',views.create_user, name='create_user'),
    path('api/v1/products/',views.all_product, name='all_product'),
    path('api/v1/products/create/',views.create_product, name='create_product'),
    path('api/v1/products/delete/<int:product_id>',views.delete_product, name='delete_product'),
    path('api/v1/products/update/<int:product_id>',views.update_product, name='update_product'),
    path('api/v1/reviews/',views.all_review, name='all_reviews'),
    path('api/v1/reviews/create/',views.post_review, name='create_reviews'),
    path('api/v1/reviews/delete/<int:review_id>',views.delete_review, name='delete_review'),
    path('api/v1/reviews/update/<int:review_id>',views.update_review, name='update_review'),
    path('api/v1/pricelisting',views.price_listing, name='price_listing'),
    path('api/v1/datelisting',views.date_listing, name='date_listing'),

]