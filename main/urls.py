from django.urls import path,include
from . import views

from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.api_form, name='api_form'),
    path('api/register', views.my_api, name='my_api'),
    path('products-ui/', views.product_ui, name='product_ui'),
    path('products-index/',views.products_index,name='products_index'),
]

