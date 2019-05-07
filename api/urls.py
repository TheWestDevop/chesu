from django.urls import path
from api.views import *

urlpatterns = [
    path('create/user/',CreateUser,name='create-user'),
    path('auth/user/',AuthUser,name='auth-user'),
    path('restaurant/',getAllRestaurants,name="all-restaurants"),
    path('meals/<int:restaurant_id>',getAllMeals,name='all-meals'),
    path('add/order/',addOrder,name='add-order'),
    path('latest/order/',getLatestOrder,name='get-latetest-order'),
    path('driver/location/',getDriverLocation,name='driver-location'),
    path('restaurant/order/notification/<slug:lastTime>/',restaurantOrderNotification,name='restaurant-order-notification'),
    path('ready/order/',getReadyOrder,name='ready-order'),
    path('driver/pickorder/',driverPickOrder,name='driver-pick-order'),
    path('latest/driver/',getLatestDriver,name='get-latest-order'),
    path('driver/complete/order/',driverCompleteOrder,name='driver-complete-order'),
    path('driver/revenue/',driverGetRevenue,name='driver-get-revenue'),
    path('driver/update/location/',driverUpdateLocation,name='driver-update-location'),

]