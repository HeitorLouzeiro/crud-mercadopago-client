from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('filter/', views.filter, name='filter'),
    path('update/', views.update, name='update'),
    path('payment/', views.payment, name='payment'),
    path('checkoutpro/', views.checkoutpro, name='checkoutpro'),
]
