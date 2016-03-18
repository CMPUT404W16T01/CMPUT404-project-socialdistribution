from django.shortcuts import render, redirect
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
        displayName = request.POST.get('fname') + " " + request.POST.get('lname')
        password = request.POST.get('pass')
        email = request.POST.get('email')
        DITTO_HOST = request.get_host()
        id = uuid.uuid4()
        user = User.objects.create_user(username=email, password=password)
        user.save()

        url = 'http://' + DITTO_HOST + "/author/" + str(id)
        new_author = Author(id=id, displayName=displayName, email=user, host=DITTO_HOST, url=url)
        new_author.save()
        return redirect("/register/confirm")
    except:
        return redirect("/register/fail")
