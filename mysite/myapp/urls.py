from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('useful/', views.delete_random),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('galls/', views.galls_view),
    path('gallery/', views.gallery_view),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view),
    path('service/', views.service_view),
]