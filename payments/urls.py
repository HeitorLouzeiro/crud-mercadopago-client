from django.urls import path

from . import views

urlpatterns = [
    path('', views.checkoutproselectedproductssession,
         name='checkoutproselectedproductssession'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('removecart/', views.removecart, name='removecart'),
    path('success/', views.success, name='success'),
    path('checkoutpro/v3', views.checkoutproselectedproducts,
         name='checkoutproselectedproducts'),
    path('checkoutpro/v2', views.checkoutproseveralproducts,
         name='checkoutproseveralproducts'),
    path('checkoutpro/v1', views.checkoutpro, name='checkoutpro'),
    path('create/', views.home, name='home'),
    path('filter/', views.filter, name='filter'),
    path('update/', views.update, name='update'),
]
