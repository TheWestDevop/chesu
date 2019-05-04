from django.urls import path
from api.views import *

urlpatterns = [
    path('restaurant/',getAllRestaurants,name="all-restaurants"),
    path('meals/<int:restaurant_id>',getAllMeals,name='all-meals'),
    path('addorder/',addOrder,name='add-order'),
    path('getlatestorder/',getLatestOrder,name='get-latetest-order'),
    path('getdriverlocation/',getDriverLocation,name='driver-location'),
    path('restaurantordernotification/<slug:lastTime>/',restaurantOrderNotification,name='restaurant-order-notification'),
    path('readyorder/',getReadyOrder,name='ready-order'),
    path('driverpickorder/',driverPickOrder,name='driver-pick-order'),
    path('getlatestorder/',getLatestDriver,name='get-latest-order'),
    path('drivercompleteorder/',driverCompleteOrder,name='driver-complete-order'),
    path('drivergetrevenue/',driverGetRevenue,name='driver-get-revenue'),
    path('driverupdatelocation/',driverUpdateLocation,name='driver-update-location'),

]