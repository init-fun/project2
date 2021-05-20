from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post

# pagination imports
from django.core.paginator import Page, EmptyPage, PageNotAnInteger, Paginator


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # post = Post.published.all()

    context = {
        "posts": posts,
        "page": page,
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
