from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from feed.models import Author


@login_required
# Create your views here.
def friends(request):
	all_authors = Author.objects.all()
	context = {
		'authors': all_authors,
	}
	return render(request, 'friends.html', context)
