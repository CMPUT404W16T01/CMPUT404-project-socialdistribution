from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from feed.models import Author
import uuid
import base64
from django.contrib.auth.models import User




# Create your views here.
def register(request):
	return render(request, 'register.html')

def confirm(request):
	return render(request, 'confirm.html')

def fail(request):
	return render(request, 'fail.html')

def sign_up(request):
	display_name = request.POST.get('fname') + " " + request.POST.get('lname')
	password = request.POST.get('pass') 
	email = request.POST.get('email')
	DITTO_HOST = request.get_host()
	user_id = uuid.uuid4()
	try:
		user = User.objects.create_user(username = email)
		user.save()
		new_author = Author(user_id = user_id, display_name = display_name, email = user, password = password, host=DITTO_HOST)
		new_author.save()
		return redirect("/register/confirm")
	except:
		return redirect("/register/fail")








