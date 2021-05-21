from datetime import datetime
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

from django.utils import timezone
from django.contrib.auth.models import User

# for creating a canonical url for our post
from django.urls import reverse

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

    # canonical url
    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class career_post(models.Model):
    from_year = models.DateField()
    to_year = models.DateField(default=datetime.now)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return self.company_name


class SocialMedia(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()
    LandingPage = models.ForeignKey(
        "LandingPage", related_name="socialSites", on_delete=models.CASCADE
    )


class LandingPage(models.Model):
    avatar = models.ImageField(upload_to="media/images", null=True, blank=True)
    quote = models.TextField()
    intro = models.TextField()
    social_json = models.JSONField(null=True)
    resume = models.FileField(upload_to="media/docs")
    skills = models.TextField(max_length=400)

    def social_nw_creator(self, *args, **kwargs):
        self.socialSites.create()
