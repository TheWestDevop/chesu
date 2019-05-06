from django.db import models
from django.utils import timezone

class User(models.Model):
      id               = models.AutoField(primary_key=True)
      username         = models.CharField(max_length=200)
      password         = models.CharField(max_length=200)
      secret           = models.CharField(max_length=200)
      usertype         = models.IntegerField(default=0)
      isemailverified  = models.IntegerField(default=0)
      isphoneverified  = models.IntegerField(default=0)
      status           = models.IntegerField(default=0)
      createdate       = models.DateTimeField(default=timezone.now)

      def get_full_name(self):
            return self.username

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.avatar

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.avatar

class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='meal')
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0)    

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant , on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank = True, null = True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    meal = models.ForeignKey(Meal , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Admin(models.Model):
       id            = models.AutoField(primary_key=True)
       username      = models.CharField(max_length=20)
       password      = models.CharField(max_length=200)
       secret        = models.CharField(max_length=20)
       admintype     = models.IntegerField()
       status        = models.IntegerField()
       createdate    = models.DateTimeField(default=timezone.now)

class AdminType(models.Model):
       id            = models.AutoField(primary_key=True)
       name      = models.CharField(max_length=20)

# Create your models here.
class UserType(models.Model):
      id   = models.AutoField(primary_key=True)
      name = models.CharField(max_length=20)

