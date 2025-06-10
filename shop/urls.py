from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home, name='home'),  # This handles the root '/'
    path('home',views.home,name='home'),
    path('login',views.loginpage,name='login'),
    path('loginout',views.loginoutpage,name='loginout'),
    path('cart',views.cart,name='cart'),

    path('removecart/<str:cid>',views.removecart,name='removecart'),
    path('register',views.register,name='register'),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.productdetails,name="productdetails"),
    path('addtocart',views.addtocart,name='addtocart'),

]
