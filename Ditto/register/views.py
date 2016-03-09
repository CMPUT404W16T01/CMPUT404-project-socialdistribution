from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from feed.models import Author
import uuid
from django.contrib.auth.models import User




# Create your views here.
def register(request):
	if request.user.is_authenticated():
		return redirect('/feed')
	else:
		return render(request, 'register.html')

def confirm(request):
	if request.user.is_authenticated():
		return redirect('/feed')
	else:
		return render(request, 'confirm.html')

def fail(request):
	if request.user.is_authenticated():
		return redirect('/feed')
	else:
		return render(request, 'fail.html')

def sign_up(request):
	try:
		display_name = request.POST.get('fname') + " " + request.POST.get('lname')
		password = request.POST.get('pass') 
		email = request.POST.get('email')
		DITTO_HOST = request.get_host()
		user_id = uuid.uuid4()
		user = User.objects.create_user(username = email, password = password)
		user.save()
		new_author = Author(user_id = user_id, display_name = display_name, email = user, host=DITTO_HOST)
		new_author.save()
		return redirect("/register/confirm")
	except:
		return redirect("/register/fail")








