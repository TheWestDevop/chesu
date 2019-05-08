from django.urls import path
from manager.views import *

urlpatterns = [
    
    path('restaurant/auth/',Auth,name="auth"),
    path('restaurant/authAdmin/',authAdmin,name="authAdmin"),
    path('restaurant/Admin/login',loginAdmin,name="loginAdmin"),
    path('restaurant/Admin/create/user',CreateUser,name="admin-create-user"),
    path('restaurant/Admin/users',allUser,name="all-user"),
    path('restaurant/Admin/restaurant',allRestaurant,name="all-restaurant"),
    
]