from django.shortcuts import render

# Create your views here.
def friends(request):
	return render(request, 'friends.html')
