from models.models import *
from django.core.paginator import *
from django.http import JsonResponse
from django.views.decorators.http import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
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
              "logo":restaurant.logo,
              "user id":user.id
           }
           items.append(item) 
        data['data'] = items
        data['message'] = "successfully fetched restaurants"     

        return JsonResponse(data)


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
              "image":meal.image,
              "price":meal.price,
              "restaurant id":restaurant.id
           }
           items.append(item) 
        data['data'] = items
        data['message'] = "successfully fetched restaurants"     

        return JsonResponse(data)

@csrf_exempt
def addOrder(request):
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

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

@csrf_exempt
def getLatestOrder(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = Order.objects.filter(customer = customer).last()

    return JsonResponse({"order": order})

def getDriverLocation(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer = customer, status = Order.DELIVERED).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})    

def restaurantOrderNotification(request, lastTime):
    notification = Order.objects.filter(restaurant = request.user.restaurant,
        created_at__gt = last_Time).count()

    return JsonResponse({"notification": notification})

def getReadyOrder(request):
    orders = Order.objects.filter(status = Order.READY, driver = None).order_by("-id")   
    return JsonResponse({"orders": orders}) 

@csrf_exempt
def driverPickOrder(request):
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

        # Get Driver
        driver = access_token.user.driver

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

    return JsonResponse({})

def getLatestDriver(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})

@csrf_exempt
def driverCompleteOrder(request):
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})


def driverGetRevenue(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

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

@csrf_exempt
def driverUpdateLocation(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})











