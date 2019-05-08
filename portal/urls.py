from django.urls import path
from .views import *

urlpatterns = [
	path('vendor/dashboard/',userHome,name="dashboard"),
    path('vendor/sign-up',SignUp,name="sign-up"),
    path('vendor/',Login,name="login"),
    path('vendor/sign-out/',Logout,name="logout"),
    path('',Login,name="home"),
    path('vendor/order/',OrderMeal,name="order"),
    path('vendor/account',Account,name="account"),
    path('vendor/meal',Meals,name="meal"),
    path('vendor/addmeal',AddMeal,name="addmeal"),
    path('vendor/editmeal/<int:id>/',EditMeal,name="edit-meal"),
    path('vendor/customer',customer,name="customer"),
    path('vendor/report',Report,name="report"),
   
]