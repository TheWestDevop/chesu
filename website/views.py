from django.shortcuts import render

# Create your views here.

data={}
def index(request):
	context={}
	return render(request, 'website/index.html',context)
	
	
def login(request):
	context={}
	return render(request, 'website/login.html',context)
	
def register(request):
	context={}
	return render(request, 'website/register.html',context)