from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dogs-home'),
    path('about/', views.about, name='dogs-about')
]
