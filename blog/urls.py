from django.urls import path
from . import views

app_name = "blog"  # namespacing

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("comingsoon/", views.coming_soon, name="coming_soon"),
    path("posts/", views.posts_homepage, name="posts_homepage"),
    path("posts/tag/<slug:tag_slug>/", views.posts_homepage, name="tagged"),
    path("show/", views.show_base_post, name="show"),
]
