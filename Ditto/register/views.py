from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.
def register(request):
	return render(request, 'register.html')

def sign_up(request):
	print request.POST.get('fname') 
	print request.POST.get('lname')  
	print request.POST.get('email')
	print request.POST.get('pass') 
	return HttpResponse(request.POST.get('fname'))

	# if x is empty, return and ask for X

	#return render(request, request.data)
