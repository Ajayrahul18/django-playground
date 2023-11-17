from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.get_products, name='get_products'),
    path('product/new/', views.new_product, name='new_product'),
    path('product/update_images/', views.update_product_image, name='update_product_image'),
    path('product/<str:pk>/', views.get_product, name='get_product'),
    path('product/<str:pk>/update/', views.update_product, name='update_product'),
    path('product/<str:pk>/delete/', views.delete_product, name='delete_product'),
    path('<str:pk>/review/', views.create_update_reviews, name='create_update_reviews'),
    path('<str:pk>/review/delete/', views.delete_reviews, name='delete_reviews'),
    
]
