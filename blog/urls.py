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
    path("comingsoon", views.coming_soon, name="coming_soon"),
    path("posts", views.PostListView.as_view(), name="postlist"),
    path("show", views.show_base_post, name="show"),
]
