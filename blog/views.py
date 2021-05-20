from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import career_post

# pagination imports
from django.core.paginator import Page, EmptyPage, PageNotAnInteger, Paginator


year_list = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def post_list(request):
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
        "year_list": year_list,
        "career_range": range(2),
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
