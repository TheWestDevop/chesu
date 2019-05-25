from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
	path('home',home,name='user-home'),
	path('login',login,name="user-login"),
	path('logout',Logout,name="user-logout"),
	path('auth',auth,name="auth-new-user"),
	path('register',register,name="user-register"),
	path('signup',SignUp,name="user-sign-up")
   
]