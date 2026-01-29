from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('like/<int:product_id>/', views.like_product, name='like_product'),
    path('dislike/<int:product_id>/', views.dislike_product, name='dislike_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path("recommendations/", views.recommended_products, name="recommendations"),

]
