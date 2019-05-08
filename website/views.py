from django.shortcuts import render

# Create your views here.

data={}
def index(request):
	context={}
    return render(request, 'website/index.html',context)