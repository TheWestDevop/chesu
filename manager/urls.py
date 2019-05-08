from django.urls import path
from .views import *

urlpatterns = [
    
    
	path('gen',genadmin,name="genadmin"),
    path('authAdmin',authAdmin,name="authAdmin"),
    path('login',loginAdmin,name="loginAdmin"),
    path('create/user',CreateUser,name="CreateUser"),
    path('users',allUser,name="users"),
    path('restaurant',allRestaurant,name="restaurant"),
    
]