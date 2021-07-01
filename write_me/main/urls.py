from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('login/', views.sign_in, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('verify/<int:profile_id>', views.verify, name='verify'),
    path('chat/<int:profile_id>', views.chat, name='chat'),
]