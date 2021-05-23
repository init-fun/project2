from typing import List
from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.urls.base import is_valid_path
from .models import Post
from .models import career_post
from .models import LandingPage
from .models import Project

# class based views
from django.views.generic import ListView

# comment system
from .models import Comment
from .forms import CommentForm

# pagination imports
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def post_list(request):
    # projects
    all_project = Project.objects.all()
    first_two = all_project[:2]
    # landing page objects

    index_obj = LandingPage.objects.first()
    web_obj = index_obj.social_json
    all_skills = index_obj.skills.split("\r\n \r\n")
    # end of landing page objects

    # blog related objects
    bp_object_list = Post.published.all().order_by("-publish")
    paginator = Paginator(bp_object_list, 2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    all_posts = Post.published.all()

    # career related objects
    workplaces = career_post.objects.all()
    context = {
        "posts": posts,  # get the posts for the page number
        "page": page,  # this has 2 pages
        "all_posts": all_posts,
        # career related context obj
        "company": workplaces,
        "first_two_company": workplaces[:2],
        "career_range": range(2),
        "index_obj": index_obj,
        "web_obj": web_obj,
        "all_skills": all_skills,
        "first_two_project": first_two,
        "all_projects": all_project,
    }
    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # list of active comments
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }
    return render(request, "blog/post/detail.html", context)


def coming_soon(request):
    return render(request, "blog/post/comingsoon.html", {})


# To display post we have two options here
# 1. list based
# 2. Class based


def all_posts(request):
    object_list = Post.published.all()
    # print(object_list)
    paginator = Paginator(object_list, 6)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/all_posts.html", {"page": page, "posts": posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 6
    template_name = "blog/post/post_list.html"


def show_base_post(request):
    return render(request, "blog/post/post_base.html", {})
