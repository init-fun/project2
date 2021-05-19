from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# a model manager to get all published posts
class PublishedObjManager(models.Manager):
    def get_queryset(self):
        return (
            super(PublishedObjManager, self).get_queryset().filter(status="published")
        )


class Post(models.Model):
    objects = models.Manager()  # default manager
    published = PublishedObjManager()  # custome object manager
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date="publish"
    )  # this publish is connected to publish field
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title
