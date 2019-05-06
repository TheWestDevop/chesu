from django.urls import path
from manager.views import *

urlpatterns = [
    path('restaurant/dashboard/',userHome,name="dashboard"),
    path('restaurant/sign-up',SignUp,name="sign-up"),
    path('restaurant/auth/',Auth,name="auth"),
    path('restaurant/',Login,name="login"),
    path('restaurant/sign-out/',Logout,name="logout"),
    path('',Login,name="home"),
    path('restaurant/order/',OrderMeal,name="order"),
    path('restaurant/account',Account,name="account"),
    path('restaurant/meal',Meals,name="meal"),
    path('restaurant/addmeal',AddMeal,name="addmeal"),
    path('restaurant/editmeal/<int:id>/',EditMeal,name="edit-meal"),
    path('restaurant/customer',customer,name="customer"),
    path('restaurant/add/customer',AddCustomer,name="add-customer"),
    path('restaurant/report',Report,name="report"),
]