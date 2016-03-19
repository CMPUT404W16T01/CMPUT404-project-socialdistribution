from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from feed.models import Author
from django.contrib.auth.models import User



@login_required
# Create your views here.
def friends(request):
	user_object = User.objects.get(username = request.user.username)
	author_object = Author.objects.get(email = user_object)

	all_authors = Author.objects.all()
	context = {
		'authors': all_authors,
		'current_author': author_object,
	}
	return render(request, 'friends.html', context)
