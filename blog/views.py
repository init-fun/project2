from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import career_post
from .models import LandingPage

# pagination imports
from django.core.paginator import Page, EmptyPage, PageNotAnInteger, Paginator


def post_list(request):
    # landing page objects
    index_obj = LandingPage.objects.first()
    web_obj = index_obj.social_json
    all_skills = index_obj.skills.split("\r\n \r\n")
    # end of landing page objects

    # blog related objects
    object_list = Post.published.all().order_by("-publish")
    paginator = Paginator(object_list, 2)
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
        "posts": posts,
        "page": page,
        "all_posts": all_posts,
        # career related context obj
        "company": workplaces,
        "first_two_company": workplaces[:2],
        "career_range": range(2),
        "index_obj": index_obj,
        "web_obj": web_obj,
        "all_skills": all_skills,
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

    context = {
        "post": post,
    }
    return render(request, "blog/post/detail.html", context)
