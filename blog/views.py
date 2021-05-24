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

# similar post
from django.db.models import Count

# tagging
from taggit.models import Tag

# comment system
from .models import Comment
from .forms import CommentForm

# pagination imports
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def post_list(request):

    # landing page objects
    # first two projects for the landing page
    all_project = Project.objects.all()
    first_two = all_project[:2]
    # img, text, quote , skills, resume etc
    index_obj = LandingPage.objects.first()
    web_obj = index_obj.social_json
    all_skills = index_obj.skills.split("\r\n \r\n")
    # end of landing page objects

    # blog related objects
    posts = Post.published.all().order_by("-publish")
    first_two_posts = posts[:2]
    # career related objects
    wp = career_post.objects.all()
    first_two_wp = wp[:2]

    context = {
        "first_two_posts": first_two_posts,  # get the posts for the page number
        "posts": posts,
        "first_two_company": first_two_wp,
        "index_obj": index_obj,
        "web_obj": web_obj,
        "all_skills": all_skills,
        "first_two_project": first_two,
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
    # similar posts
    posts_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=posts_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "similar_posts": similar_posts,
    }

    return render(request, "blog/post/post_detail.html", context)


def coming_soon(request):
    return render(request, "blog/post/comingsoon.html", {})


# To display post we have two options here
# 1. list based
# 2. Class based


def posts_homepage(request, tag_slug=None):
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

    # tagging
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = object_list.filter(tags__in=[tag])

    context = {
        "page": page,
        "posts": posts,
        "tag": tag,
    }

    return render(request, "blog/post/post_list.html", context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 6
    template_name = "blog/post/post_list.html"


def show_base_post(request):
    return render(request, "blog/post/post_base.html", {})


def post_sidebar(request):
    return render(request, "blog/post/sidebar.html", {})
