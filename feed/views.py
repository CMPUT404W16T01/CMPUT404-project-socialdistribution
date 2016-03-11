from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from feed.models import Post
from feed.models import Author
from feed.models import Comment
from django.contrib.auth.models import User
import json
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
import CommonMark


# Create your views here.

@login_required
def feed(request):
    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)

    github_name = author_object.github_account

    # My feed, access all posts that I can see
    self_posts = Post.objects.filter(author_id=author_object)
    public_posts = Post.objects.filter(visibility="public")
    all_comments = Comment.objects.all()
    # friend_posts
    # foaf_posts
    server_posts = Post.objects.filter(visibility="server")
    main_posts = self_posts | public_posts | server_posts
    for post in main_posts:
        # print post.post_id
        comment_list = []
        if (str(author_object.user_id) == str(post.author_id)):
            post.flag = True
        else:
            post.flag = False

        for comment in all_comments:
            if (str(comment.post_id) == str(post.post_id)):
                comment_list.append(comment)
        post.comments = comment_list
        print post.comments
    # end of my feed

    # Begin Public Feed
    # public_posts was already created for use in the other one
    for post in public_posts:
        # print post.post_id
        if (str(author_object.user_id) == str(post.author_id)):
            post.flag = True
        else:
            post.flag = False
    # end of public feed

    # Begin My Posts
    # self_posts was already created for use
    for post in self_posts:
        # print post.post_id
        if (str(author_object.user_id) == str(post.author_id)):
            post.flag = True
        else:
            post.flag = False
    # end of public feed




    context = {
        'main_posts': main_posts,
        'public_posts': public_posts,
        'my_posts': self_posts,
        "github_account": github_name,
    }

    return render(request, 'feed.html', context)


def delete(request):
    post_id = request.POST.get('post_post_id')
    Post.objects.filter(post_id=post_id).delete()
    return redirect('/feed')


def logout(request):
    auth_logout(request)
    return redirect('/login')


def create_comment(request):
    body = request.POST.get('comment-input')
    parent_id = request.POST.get('comment-parent-id')
    print parent_id
    is_markdown = request.POST.get('comment-is-markdown')
    print type(is_markdown)
    if is_markdown:
        body = CommonMark.commonmark(body)
        is_markdown = True
    else:
        is_markdown = False
    print body
    print is_markdown

    date_published = datetime.datetime

    post_object = Post.objects.get(post_id=parent_id)
    c_username = request.user.username
    user_object = User.objects.get(username=c_username)
    author_object = Author.objects.get(email=user_object)

    print post_object.title
    print author_object.email

    new_comment = Comment(author_id=author_object, post_id=post_object, body=body, is_markdown=is_markdown,
                          date_published=date_published)
    print("comment made")

    new_comment.save()
    return redirect('/feed')


def create_post(request):
    body = request.POST.get('post_body')
    date_published = datetime.datetime
    is_markdown = json.loads(request.POST.get('is_markdown'))

    if is_markdown:
        body = CommonMark.commonmark(body)
    visibility = request.POST.get('visibility')
    c_username = request.user.username
    user_object = User.objects.get(username=c_username)
    author_object = Author.objects.get(email=user_object)

    DITTO_HOST = request.get_host()
    title = request.POST.get('title')
    description = request.POST.get('description')

    categories = request.POST.get('categories')

    c = categories.split(' ')

    categories_json = json.dumps(c)

    new_post = Post(date_published=date_published, author_id=author_object, body=body, is_markdown=is_markdown,
                    visibility=visibility, source=DITTO_HOST, origin=DITTO_HOST, categories=categories, title=title,
                    description=description)
    new_post.save()

    return HttpResponse(request.POST.get('post_body'))
