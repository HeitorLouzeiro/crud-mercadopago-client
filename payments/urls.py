from django.urls import path

from . import views

urlpatterns = [
    path('', views.checkoutpro, name='checkoutpro'),
    path('create/', views.home, name='home'),
    path('filter/', views.filter, name='filter'),
    path('update/', views.update, name='update'),
]
