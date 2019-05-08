from django.shortcuts import render, redirect


from models.models import *
from django.db.models import Sum, Count, Case, When
from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
import string
import hashlib

# Create your views here.
def Home(request):
    return redirect('login')

def userHome(request):
    if request.session.has_key('userId'):
         return redirect(OrderMeal)
    else:
        return redirect('login')
		
def Auth(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        plainpassword = request.POST.get('password')
        
        
    try:
            user = User.objects.get(username=username)

            secret = user.secret
            
            passwordConfirm = hashPassword(plainpassword+secret)
        

            if passwordConfirm == user.password :
              request.session['userId'] = user.id
              
              return redirect('order')
              pass
        
            else:
               errormsg = "Invalid Username or Password"
               messages.error(request,errormsg)
               return redirect('login')
               pass
    except ObjectDoesNotExist:

        errormsg = "User Doesn't Exist"
        messages.error(request, errormsg)
        return redirect('login')
        pass

    else:
        return redirect('login')


def SignUp(request):
    user = []
    restaurant = []
    if request.method == "POST":
        # User Data
        username = request.POST.get('username')
        plainpassword = request.POST.get('password')
        email = request.POST.get('email')
        secret = secretGenerator()
        password = hashPassword(str(plainpassword)+secret)
      
        # Restaurant Data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        logo = request.FILES['logo']
        fs = FileSystemStorage()
        filename = fs.save(logo.name.strip(), logo)

        user = User.objects.create(username=username,password=password,secret=secret )
        restaurant = Restaurant.objects.create(
            user=user,
            name=name,
            phone=phone,
            address=address,
            logo=filename,
            email=email
            )

        errormsg = "Login to access your restaurant"
        messages.error(request,errormsg)
        return redirect('login')

    return render(request, "portal/sign_up.html", {
        "userform": user,
        "restaurantform": restaurant
    })
	

def Login(request):
    return render(request, 'portal/sign_in.html')


def Logout(request):
    logout(request)
    return redirect(Login)
	


def OrderMeal(request):
    if request.session.has_key('userId'):
         userid = request.session.get('userId')
         restaurant = Restaurant.objects.get(user_id=userid)
         user = User.objects.get(id=userid)

         if request.method == "POST":
               order = Order.objects.get(
               id=request.POST["id"], restaurant=restaurant)

               if order.status == Order.COOKING:
                   order.status = Order.READY
                   order.save()

         orders = Order.objects.filter(
            restaurant=restaurant).order_by("-id")
         return render(request, 'portal/order.html', {"orders": orders, "restaurant": restaurant, "user": user})
    else:
           return redirect('login')

def Account(request):
    if request.session.has_key('userId'):
        if request.method == "POST":

              # User Data
             username = request.POST.get('username')
             plainpassword = request.POST.get('password')
             firstname = request.POST.get('first_name')
             lastname = request.POST.get('last_name')
             email = request.POST.get('email')
             secret = secretGenerator()
             password = hashPassword(str(plainpassword)+secret)
      
            # Restaurant Data
             name = request.POST.get('name')
             phone = request.POST.get('phone')
             address = request.POST.get('address')
             logo = request.FILES['logo']
             fs = FileSystemStorage()
             filename = fs.save(logo.name, logo)

             user = User.objects.create(
                   username=username,
                   password=password,
                   secret=secret
                   )
             restaurant = Restaurant.objects.create(
                         user=user,
                         name=name,
                         phone=phone,
                         address=address,
                         logo=filename,
                         email=email
                         )
             return render(request, 'portal/account.html', {
              "user": user,
              "restaurant": restaurant
                })
    
        

        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        restaurant = Restaurant.objects.get(user_id=userid)
        return render(request, 'portal/account.html', {"user": user,"restaurant":restaurant})
    else:
           return redirect('login')


def Meals(request):
    if request.session.has_key('userId'):
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        restaurantname = Restaurant.objects.get(user_id=userid)

        meals = Meal.objects.filter(restaurant=restaurantname).order_by("-id")

        return render(request, 'portal/meal.html', {"meals": meals,"user": user,"restaurant":restaurantname})

    else:
        return redirect('login')



def AddMeal(request):
    if request.session.has_key('userId'):
      userid = request.session.get('userId')
      user = User.objects.get(id=userid)
      restaurant = Restaurant.objects.get(user_id=userid)
      if request.method == "POST":
        name = request.POST.get('name')
        shortdesc = request.POST.get('short_description')
        price = request.POST.get('price')
        restaurant_id = request.POST.get('restaurant_id')
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name.strip(), image)

        meal = Meal.objects.create(
            name=name,
            short_description=shortdesc,
            image=filename,
            price=price,
            restaurant_id=restaurant_id
            )

        return redirect('meal')

      return render(request,'portal/add_meal.html', {"user": user,"restaurant":restaurant})
    else:     
       return redirect('login')




def EditMeal(request, id):
    if request.session.has_key('userId'):

        meal = Meal.objects.get(id=id)
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        restaurant = Restaurant.objects.get(user_id=userid)
        if request.method == "POST":
            meal.name = request.POST.get('name')
            meal.short_description = request.POST.get('short_description')
            meal.price = request.POST.get('price')
            restaurant = request.POST.get('restaurant_id')
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name.strip(), image)
            meal.image = filename
            meal.save()
            return redirect('meal')

        return render(request, 'portal/edit_meal.html', {"meal": meal,"user":user,"restaurant":restaurant})
     
    else:     
       return redirect('login')


def customer(request):
    if request.session.has_key('userId'):
         try:   
             userid = request.session.get('userId')
             user = User.objects.get(id=userid)
             restaurant = Restaurant.objects.get(user_id=userid)
         
             customers = Customer.objects.get(user_id=userid)

             orders = Order.objects.filter(restaurant=restaurant).order_by("-id")
             meal = Meal.objects.filter(restaurant=restaurant).order_by("-id")
             return render(request, 'portal/customer.html', {"customers": customers,"meal":meal,"user":user,"restaurant":restaurant})
         except ObjectDoesNotExist:
              return render(request, 'portal/customer.html', {"user":user,"restaurant":restaurant})
              pass
    else:     
       return redirect('login')


def Report(request):
    if request.session.has_key('userId'):
       userid = request.session.get('userId')
       user = User.objects.get(id=userid)
       restaurant = Restaurant.objects.get(user_id=userid)
        # Calculate revenue and number of order by current week
       from datetime import datetime, timedelta

       revenue = []
       orders = []

     # Calculate weekdays
       today = datetime.now()
       currentweekdays = [
       today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

       for day in currentweekdays:
        deliveredorders = Order.objects.filter(
            restaurant=restaurant,
            status=Order.DELIVERED,
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day
        )
        revenue.append(sum(order.total for order in deliveredorders))
        orders.append(deliveredorders.count())

       # Top 3 Meals
        top3meals = Meal.objects.filter(restaurant = restaurant).annotate(total_order = Sum('orderdetails__quantity')).order_by("-total_order")[:3]
        meal = {
        "labels": [meal.name for meal in top3meals],
        "data": [meal.total_order or 0 for meal in top3meals]
         }
    
      # Top 3 Drivers
        top3drivers = Driver.objects.annotate(
        total_order=Count(
            Case(
                When(order__restaurant=restaurant, then=1)
               )
           )
         ).order_by("-total_order")[:3]

        driver = {
        "labels": [driver.user.get_full_name() for driver in top3drivers],
        "data": [driver.total_order for driver in top3drivers]
        }

        return render(request, 'portal/report.html', {
        "revenue": revenue,
        "orders": orders,
        "meal": meal,
        "driver": driver,
        "user":user,
        "restaurant":restaurant


        })
    else:
         return redirect('login')    
		 

	
	
def secretGenerator():
    letters = string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(10))


def hashPassword(word):
    password = hashlib.sha256(word.encode()).hexdigest()
    return password