from django.contrib import admin
from .models import Post, career_post, LandingPage, Project, Comment

admin.site.register(career_post)
admin.site.register(LandingPage)
admin.site.register(Project)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "post", "created", "active")
    list_filter = ("active", "created", "updated", "name")
    search_fields = ("name", "body")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
