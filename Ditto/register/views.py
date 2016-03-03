from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.
def register(request):
	#template = loader.get_template("register.html")
	#return HttpResponse(template.render())
	return render(request, 'register.html')
