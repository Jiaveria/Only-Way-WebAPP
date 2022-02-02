from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('loginUser', views.loginUser, name='loginUser'),
    path('signup', views.signup, name='signup'),
    path('market', views.productsMarket.as_view(), name='market'),
    path('product/<int:id>/', views.productDetailView.as_view(), name='product'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/cartPage', views.remove_from_cart, name='remove-from-cart'),
    path('cartPage', views.cartPage, name='cartPage'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
 
    
]
