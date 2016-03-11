from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def friends(request):
	return render(request, 'friends.html')
