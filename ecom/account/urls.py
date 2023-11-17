from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('me/', views.current_user, name='current_user'),
    path('me/update/', views.update_user, name='update_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
