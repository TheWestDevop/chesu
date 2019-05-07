from models.models import *
from django.core.paginator import *
from django.http import JsonResponse
from django.views.decorators.http import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import *
from django.core.files.storage import FileSystemStorage
import random
import string
import hashlib
# Create your views here.

@require_http_methods("POST")
@csrf_exempt
def CreateUser(request):
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
        filename = fs.save(logo.name, logo)

        user = User.objects.create(username=username,password=password,secret=secret )
        restaurant = Restaurant.objects.create(
            user=user,
            name=name,
            phone=phone,
            address=address,
            logo=filename,
            email=email
            )
        return JsonResponse({"status": "account successfully created"})  
    else:
        return JsonResponse({"status": "failed try again"})


@require_http_methods("POST")
@csrf_exempt
def AuthUser(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        plainpassword = request.POST.get('password')
        try:
            user = User.objects.get(username=username)

            secret = user.secret
            
            passwordConfirm = hashPassword(plainpassword+secret)
        

            if passwordConfirm == user.password :
              request.session['userId'] = user.id
              return JsonResponse({"status": "you are logged in"}) 
              pass
        
            else:
                return JsonResponse({"status": "invalid credentials"}) 
                pass
        except ObjectDoesNotExist:
            return JsonResponse({"status": "User does not exist"}) 
            pass

    else:
        return JsonResponse({"status": "invalid request"}) 
    return JsonResponse({"status": "invalid request"}) 


@require_http_methods("GET")
def getAllRestaurants(request):
        restaurants = Restaurant.objects.all().order_by("-id");
        page = request.GET.get('page',1)
        paginator = Paginator(restaurants,10)
        try:
           pages = paginator.page(page)
        except PageNotAnInteger:
               pages = paginator.page(1) 
        except EmptyPage:
                pages = paginator.page(paginator.num_pages)       
        data = {}
        data['total']=Restaurant.objects.count()
        data['page']=pages.start_index()
        data['data']=[]
        items = []
        for restaurant in restaurants:
          for user in  User.objects.raw("SELECT b.id FROM models_user b WHERE b.id = %s ",[restaurant.id]):
           item = {
              "id":restaurant.id,
              "name":restaurant.name,
              "phone":restaurant.phone,
              "address":restaurant.address,
              "logo":str(restaurant.logo),
              "user id":user.id
           }
           items.append(item) 
        data['data'] = items
        data['message'] = "successfully fetched restaurants"     

        return JsonResponse(data)



@require_http_methods("GET")
def getAllMeals(request,restaurant_id):
        meals = Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id")
        page = request.GET.get('page',1)
        paginator = Paginator(meals,10)
        try:
           pages = paginator.page(page)
        except PageNotAnInteger:
               pages = paginator.page(1) 
        except EmptyPage:
                pages = paginator.page(paginator.num_pages)       
        data = {}
        data['total']=Restaurant.objects.count()
        data['page']=pages.start_index()
        data['data']=[]
        items = []
        for meal in meals:
          for restaurant in  Restaurant.objects.raw("SELECT b.id FROM models_restaurant b WHERE b.id = %s ",[meal.id]):
           item = {
              "id":meal.id,
              "name":meal.name,
              "short_desc":meal.short_description,
              "image":str(meal.image),
              "price":meal.price,
              "restaurant id":restaurant.id
           }
           items.append(item) 
        data['data'] = items
        data['message'] = "successfully fetched restaurants"     

        return JsonResponse(data)



@require_http_methods("POST")
@csrf_exempt
def addOrder(request):
  if request.session.has_key('userId'): 
    if request.method == "POST":
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        # Get profile
        customer = Customer.objects.get(user_id=userid)

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for meal in order_details:
            order_total += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:

        
            order = Order.objects.create(
                customer = customer,
                restaurant_id = request.POST["restaurant_id"],
                total = order_total,
                status = Order.COOKING,
                address = request.POST["address"]
                )

            # Step 3 - Create Order details
            for meal in order_details:
                OrderDetails.objects.create(
                    order = order,
                    meal_id = meal["meal_id"],
                    quantity = meal["quantity"],
                    sub_total = Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]
                    )

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "failed"})
  else:     
       return JsonResponse({"status": "failed", "error": "Authentication is required."})


@require_http_methods("GET")
@csrf_exempt
def getLatestOrder(request):
  if request.session.has_key('userId'):  
    userid = request.session.get('userId')
    user = User.objects.get(id=userid)
    customer = Customer.objects.get(user_id=userid)
    order = Order.objects.filter(customer = customer).last()
    return JsonResponse({"order": order})
  else:     
       return JsonResponse({"status": "failed", "error": "Authentication is required."})



@require_http_methods("GET")
def getDriverLocation(request):
  if request.session.has_key('userId'):  
    userid = request.session.get('userId')
    user = User.objects.get(id=userid)
    customer = Customer.objects.get(user_id=userid)
    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer = customer, status = Order.DELIVERED).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})    
  else:     
       return JsonResponse({"status": "failed", "error": "Authentication is required."})



@require_http_methods("GET")
def restaurantOrderNotification(request, lastTime):
     if request.session.has_key('userId'):  
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        restaurant = Restaurant.objects.get(user_id=userid)
        notification = Order.objects.filter(restaurant = restaurant,
           created_at__gt = lastTime).count()
        return JsonResponse({"notification": notification})
     else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})


@require_http_methods("GET")
def getReadyOrder(request):
    if request.session.has_key('userId'):  
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        restaurant = Restaurant.objects.get(user_id=userid)
        orders = Order.objects.filter(restaurant= restaurant,status = Order.READY, driver = None).order_by("-id")   
        return JsonResponse({"orders": orders}) 
    else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})



@require_http_methods("GET")
@csrf_exempt
def driverPickOrder(request):

    if request.session.has_key('userId'):  
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)
        if request.method == "POST":
         # Get Driver
           driver = Driver.objects.get(user_id=userid)
        # Check if driver can only pick up one order at the same time
           if Order.objects.filter(driver = driver).exclude(status = Order.DELIVERED):
              return JsonResponse({"status": "failed", "error": "You can only pick one order at the same time."})

              try:
                 order = Order.objects.get(
                 id = request.POST["order_id"],
                 driver = None,
                 status = Order.READY
                 )
                 order.driver = driver
                 order.status = Order.ONTHEWAY
                 order.picked_at = timezone.now()
                 order.save()

                 return JsonResponse({"status": "success"})

              except Order.DoesNotExist:
                    return JsonResponse({"status": "failed", "error": "This order has been picked up by another."})
    else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})




@require_http_methods("GET")
def getLatestDriver(request):
    if request.session.has_key('userId'):  
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)

        driver = Driver.objects.get(user_id=userid)
        order = OrderSerializer(
                Order.objects.filter(driver = driver).order_by("picked_at").last()
                ).data
        return JsonResponse({"order": order})
    else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})



@require_http_methods("GET")
@csrf_exempt
def driverCompleteOrder(request):
    if request.session.has_key('userId'):  
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)

        driver = Driver.objects.get(user_id=userid) 
        order = Order.objects.get(id = request.POST["order_id"], driver = driver)
        order.status = Order.DELIVERED
        order.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})



@require_http_methods("GET")
def driverGetRevenue(request):
   if request.session.has_key('userId'):  
       userid = request.session.get('userId')
       user = User.objects.get(id=userid)

       driver = Driver.objects.get(user_id=userid)

       from datetime import timedelta

       revenue = {}
       today = timezone.now()
       current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

       for day in current_weekdays:
           orders = Order.objects.filter(
               driver = driver,
               status = Order.DELIVERED,
               created_at__year = day.year,
               created_at__month = day.month,
               created_at__day = day.day
               )

           revenue[day.strftime("%a")] = sum(order.total for order in orders)

       return JsonResponse({"revenue": revenue})
   else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})




@require_http_methods("GET")
@csrf_exempt
def driverUpdateLocation(request):
    if request.session.has_key('userId'):  
       
      if request.method == "POST":
      
        userid = request.session.get('userId')
        user = User.objects.get(id=userid)

        driver = Driver.objects.get(user_id=userid)
        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "failed", "error": "Authentication is required."})



def secretGenerator():
    letters = string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(10))


def hashPassword(word):
    password = hashlib.sha256(word.encode()).hexdigest()
    return password









