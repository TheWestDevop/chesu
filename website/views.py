from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from models.models import *
import random
import string
import hashlib
# Create your views here.

data = {}


def home(request):
        if request.session.has_key('userId'):
            userid = request.session.get('userId')
            return render(request, 'website/user_index.html',{"user":User.objects.get(id=userid)})
        else:
    	    return redirect('user-login')


def index(request):
    context = {}
    return render(request, 'website/index.html', context)


def login(request):
    context = {}
    return render(request, 'website/login.html', context)


def register(request):
    return render(request, 'website/register.html')


def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        plainpassword = request.POST.get('password')

    try:
            user = User.objects.get(username=username)

            secret = user.secret

            passwordConfirm = hashPassword(plainpassword+secret)

            if passwordConfirm == user.password:
              request.session['userId'] = user.id

              return redirect('user-home')
              pass

            else:
               errormsg = "Invalid Username or Password"
               messages.error(request, errormsg)
               return redirect('user-login')
               pass
    except ObjectDoesNotExist:
        errormsg = "User Doesn't Exist"
        messages.error(request, errormsg)
        return redirect('user-login')
        pass

def Logout(request):
    logout(request)
    return redirect(login)
		                
def SignUp(request):

    if request.method == "POST":
        # User Data
        username = request.POST.get('username')
        plainpassword = request.POST.get('password')
        email = request.POST.get('email')
        secret = secretGenerator()
        password = hashPassword(str(plainpassword)+secret)
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user = User.objects.create(username=username,password=password,secret=secret, usertype = 2, address=address,phone=phone,email=email)
        return redirect('user-login')

    return redirect('user-register')

def secretGenerator():
    letters = string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(10))


def hashPassword(word):
    password = hashlib.sha256(word.encode()).hexdigest()
    return password
