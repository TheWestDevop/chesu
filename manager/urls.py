from django.urls import path
from manager.views import *

urlpatterns = [
    path('restaurant/dashboard/',userHome,name="dashboard"),
    path('restaurant/sign-up',SignUp,name="sign-up"),
    path('restaurant/auth/',Auth,name="auth"),
    path('restaurant/authAdmin/',authAdmin,name="authAdmin"),
    path('restaurant/Admin/login',loginAdmin,name="loginAdmin"),
    path('restaurant/Admin/create/user',CreateUser,name="admin-create-user"),
    path('restaurant/Admin/users',allUser,name="all-user"),
    path('restaurant/Admin/restaurant',allRestaurant,name="all-restaurant"),
    path('restaurant/',Login,name="login"),
    path('restaurant/sign-out/',Logout,name="logout"),
    path('',Login,name="home"),
    path('restaurant/order/',OrderMeal,name="order"),
    path('restaurant/account',Account,name="account"),
    path('restaurant/meal',Meals,name="meal"),
    path('restaurant/addmeal',AddMeal,name="addmeal"),
    path('restaurant/editmeal/<int:id>/',EditMeal,name="edit-meal"),
    path('restaurant/customer',customer,name="customer"),
    path('restaurant/report',Report,name="report"),
]