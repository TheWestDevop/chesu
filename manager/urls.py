from django.urls import path
from .views import *

urlpatterns = [
	path('meal',allMeals,name="meals"),
    path('gen',gen,name="gen"),
    path('authAdmin',authAdmin,name="authAdmin"),
    path('login',loginAdmin,name="loginAdmin"),
    path('logout',logoutAdmin,name="logoutAdmin"),
    path('create/user',CreateUser,name="CreateUser"),
    path('users',allUser,name="users"),
    path('restaurant',allRestaurant,name="restaurant"),
    path('order',allOrder,name="order"),
    path('customers',allCustomer,name="customers"),
    
]