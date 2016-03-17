from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from feed.models import Author
from django.contrib.auth.models import User


@login_required
def settings(request):
    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)

    # display name
    display_name = author_object.display_name

    # github account
    github_account = author_object.github_account

    # github flag
    github_flag = author_object.github_flag

    if github_flag:
        github_flag = 'checked'
        print github_flag
    else:
        github_flag = ''
        print 'not checked'

    context = {
        'display_name': display_name,
        'github_account': github_account,
        'github_flag': github_flag,
    }

    return render(request, 'settings.html', context)


def save_settings(request):
    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)
    display_name = request.POST.get('display_name')
    new_password = request.POST.get('new_password').strip()
    retype = request.POST.get('retype').strip()
    github_account = request.POST.get('github_name')
    github_flag = request.POST.get('test6')

    if github_flag == 'true':
        github_flag = True
    elif github_flag == 'false':
        github_flag = False

    if len(new_password) > 0 and len(retype > 0):
        if new_password == retype:
            password = new_password
            user_object.set_password(new_password)

    author_object.display_name = display_name
    author_object.github_account = github_account
    author_object.github_flag = github_flag

    user_object.save()
    author_object.save()

    return HttpResponse(request)
