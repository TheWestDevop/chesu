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

	

def authAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        plainpassword = request.POST.get('password')
        
        
    try:
            user = Admin.objects.get(username=username)

            secret = user.secret
            
            passwordConfirm = hashPassword(plainpassword+secret)
        

            if passwordConfirm == user.password :
              request.session['userId'] = user.id
              
              return redirect('users')
              pass
        
            else:
               errormsg = "Invalid Username or Password"
               messages.error(request,errormsg)
               return redirect('loginAdmin')
               pass
    except ObjectDoesNotExist:

        errormsg = "User Doesn't Exist"
        messages.error(request, errormsg)
        return redirect('loginAdmin')
        pass

    else:
        return redirect('loginAdmin')

def allUser(request):
    if request.session.has_key('userId'):
         id = request.session.get('userId')
         admin = Admin.objects.get(id=id)
         users = User.objects.all()
         return render(request, 'manager/users.html', {"users":users,"admin":admin})
    else:
        return redirect('loginAdmin') 

def allRestaurant(request):
    if request.session.has_key('userId'):
         id = request.session.get('userId')
         admin = Admin.objects.get(id=id)
         restaurant = Restaurant.objects.all()
         return render(request, 'manager/restaurant.html', {"restaurants":restaurant,"admin":admin})
    else:
        return redirect('loginAdmin') 

def allMeals(request):
     if request.session.has_key('userId'):
         id = request.session.get('userId')
         admin = Admin.objects.get(id=id)
         meal = Meal.objects.all()
         return render(request, 'manager/meal.html', {"meals":meal,"admin":admin})
     else:
        return redirect('loginAdmin') 

def allCustomer(request):
    if request.session.has_key('userId'):
         id = request.session.get('userId')
         admin = Admin.objects.get(id=id)
         customer = Customer.objects.all()
         return render(request, 'manager/customer.html', {"customers":customer,"admin":admin})
    else:
        return redirect('loginAdmin') 

def allOrder(request):
        if request.session.has_key('userId'):
             id = request.session.get('userId')
             admin = Admin.objects.get(id=id)
             order = Order.objects.all()
             return render(request, 'manager/order.html', {"orders":order,"admin":admin})
        else:
             return redirect('loginAdmin') 


def report(request):
    pass

def CreateUser(request):
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
        return redirect('all-user')

    return redirect('all-user')

def loginAdmin(request):
    return render(request, 'manager/sign_in.html')

def logoutAdmin(request):
    logout(request)
    return redirect(loginAdmin)


def secretGenerator():
    letters = string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(10))


def hashPassword(word):
    password = hashlib.sha256(word.encode()).hexdigest()
    return password



