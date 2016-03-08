from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from feed.models import Author
import uuid



# Create your views here.
def register(request):
	return render(request, 'register.html')

def confirm(request):
	return render(request, 'confirm.html')

def sign_up(request):
	display_name = request.POST.get('fname') + " " + request.POST.get('lname')
	password = request.POST.get('pass') 
	email = request.POST.get('email')
	DITTO_HOST = request.get_host()
	new_author = Author(display_name = display_name, password = password, email = email, host=DITTO_HOST)
	new_author.save()
	return redirect("/register/confirm")






