from django.urls import path
from manager.views import *

urlpatterns = [
    
    path('auth',Auth,name="auth"),
	path('gen',genadmin,name="genadmin"),
    path('authAdmin/',authAdmin,name="authAdmin"),
    path('login',loginAdmin,name="loginAdmin"),
    path('create/user',CreateUser,name="admin-create-user"),
    path('users',allUser,name="all-user"),
    path('restaurant',allRestaurant,name="all-restaurant"),
    
]